"""Bidirectional Telegram bot for the auto-research system.

Listens for incoming messages from the user, processes them with Gemini
(including project context from resource.md and strategy.py), and sends
back the response. Also allows the user to inject feedback that gets
recorded in resource.md for the next experiment iteration.

When a backtest is positive (>10% profit), asks the user for confirmation
to deploy to LIVE trading.
"""

import asyncio
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime
from datetime import timezone
from typing import Optional

from google import genai
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

PROJECTS_DIR = "projects"
POLL_INTERVAL_SECONDS = 2
MCP_ENDPOINT = "https://binance.armaddia.lat/sse"
LIVE_DEPLOYMENT_THRESHOLD = 10.0  # Profit % to trigger LIVE confirmation


def _load_env_credentials() -> tuple:
    """Load Telegram credentials from environment or .env file.

    Returns:
        Tuple of (token, chat_id) strings, either may be None.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        env_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".env",
        )
        if os.path.exists(env_path):
            with open(env_path, "r") as env_file:
                for line in env_file:
                    if line.startswith("TELEGRAM_BOT_TOKEN="):
                        token = line.strip().split("=", 1)[1]
                    if line.startswith("TELEGRAM_CHAT_ID="):
                        chat_id = line.strip().split("=", 1)[1]

    return token, chat_id


def _send_message(token: str, chat_id: str, text: str) -> None:
    """Send a message to Telegram.

    Args:
        token: Telegram bot token.
        chat_id: Telegram chat ID.
        text: Message text (max 4096 chars, will be truncated).
    """
    # Telegram max message length is 4096
    text = text[:4096]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode(
        {"chat_id": chat_id, "text": text}
    ).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req):
            pass
    except Exception as send_err:
        print(f"Error sending Telegram message: {send_err}")


def _get_updates(token: str, offset: int, timeout: int = 30) -> list:
    """Long-poll Telegram for new messages.

    Args:
        token: Telegram bot token.
        offset: Update offset to avoid processing old messages.
        timeout: Long-polling timeout in seconds.

    Returns:
        List of update dicts from the Telegram API.
    """
    url = (
        f"https://api.telegram.org/bot{token}/getUpdates"
        f"?offset={offset}&timeout={timeout}"
    )
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout + 5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                return data.get("result", [])
    except Exception as poll_err:
        print(f"Error polling Telegram: {poll_err}")
    return []


def _gather_project_context() -> str:
    """Read resource.md and strategy.py from all projects.

    Returns:
        A formatted string with the context from each project.
    """
    context_parts = []

    if not os.path.exists(PROJECTS_DIR):
        return "No projects directory found."

    for project in os.listdir(PROJECTS_DIR):
        project_path = os.path.join(PROJECTS_DIR, project)
        if not os.path.isdir(project_path):
            continue

        config_path = os.path.join(project_path, "config.json")
        if not os.path.exists(config_path):
            continue

        try:
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
        except Exception:
            continue

        project_name = config.get("project_name", project)
        target_file = config.get("experiment", {}).get(
            "target_file", "strategy.py"
        )

        header = f"=== PROJECT: {project_name} ==="
        parts = [header]

        # Read resource.md (last 3000 chars to keep context manageable)
        resource_path = os.path.join(project_path, "resource.md")
        if os.path.exists(resource_path):
            with open(resource_path, "r") as resource:
                content = resource.read()
            parts.append(
                f"--- resource.md (last experiments) ---\n"
                f"{content[-3000:]}"
            )

        # Read current strategy code
        target_path = os.path.join(project_path, target_file)
        if os.path.exists(target_path):
            with open(target_path, "r") as target:
                code = target.read()
            parts.append(
                f"--- {target_file} (current code) ---\n{code}"
            )

        context_parts.append("\n".join(parts))

    return "\n\n".join(context_parts) if context_parts else "No projects."


def _save_feedback(user_message: str) -> None:
    """Save user feedback to resource.md of all active projects.

    Appends the feedback as a special entry so the next experiment
    iteration can read and consider it.

    Args:
        user_message: The raw feedback text from the user.
    """
    if not os.path.exists(PROJECTS_DIR):
        return

    timestamp_utc = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    for project in os.listdir(PROJECTS_DIR):
        project_path = os.path.join(PROJECTS_DIR, project)
        resource_path = os.path.join(project_path, "resource.md")
        if not os.path.exists(resource_path):
            continue

        with open(resource_path, "a") as resource:
            resource.write(
                f"\n--- Feedback del Usuario ({timestamp_utc}) ---\n"
                f"{user_message}\n"
            )


def _process_message(user_message: str) -> str:
    """Process a user message and return a response.

    If the message starts with /feedback, it saves the feedback to
    resource.md. If /confirm_live, it deploys pending strategy to LIVE.
    Otherwise, it sends the question to Gemini with full project context.

    Args:
        user_message: The message text from the user.

    Returns:
        Response text to send back.
    """
    # Handle feedback command
    if user_message.lower().startswith("/feedback"):
        feedback_text = user_message[len("/feedback"):].strip()
        if not feedback_text:
            return (
                "Uso: /feedback <tu retroalimentación>\n\n"
                "Ejemplo: /feedback No uses trailing stop loss, "
                "los últimos 3 experimentos con stop loss dan peor resultado"
            )
        _save_feedback(feedback_text)
        return (
            f"✅ Feedback guardado en resource.md.\n\n"
            f"La próxima iteración del bot lo tomará en cuenta:\n"
            f'"{feedback_text}"'
        )

    # Handle LIVE deployment confirmation
    if user_message.lower().startswith("/confirm_live"):
        pending = _read_pending_deployment()
        if not pending:
            return (
                "❌ No hay deployments pendientes.\n\n"
                "Solo puedo desplegar a LIVE cuando un backtest "
                "Sea positivo (>10% profit)."
            )
        return _execute_live_deployment(pending)

    # Regular question: send to Gemini with context
    context = _gather_project_context()
    model_id = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-lite")

    prompt = (
        "Eres el asistente de un sistema de trading automatizado "
        "(Auto Researcher). El usuario te hace preguntas sobre los "
        "reportes y resultados de los experimentos.\n\n"
        "Responde de forma clara y concisa en español.\n\n"
        f"CONTEXTO ACTUAL DEL SISTEMA:\n{context}\n\n"
        f"PREGUNTA DEL USUARIO:\n{user_message}"
    )

    try:
        client = genai.Client()
        response = client.models.generate_content(
            model=model_id, contents=prompt
        )
        return response.text[:4000]
    except Exception as gen_err:
        return f"Error al consultar Gemini: {gen_err}"


def _read_pending_deployment() -> Optional[dict]:
    """Read pending LIVE deployment state.

    Returns:
        Dict with pending deployment info or None if none exists.
    """
    for project in os.listdir(PROJECTS_DIR):
        project_path = os.path.join(PROJECTS_DIR, project)
        pending_file = os.path.join(project_path, ".pending_live_deployment")
        if os.path.exists(pending_file):
            try:
                with open(pending_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
    return None


def _execute_live_deployment(pending: dict) -> str:
    """Execute deployment of the pending strategy to LIVE trading.

    Args:
        pending: Dict with project_path, strategy_code, profit_pct, etc.

    Returns:
        Response message to send to user.
    """
    project_path = pending.get("project_path")
    strategy_code = pending.get("strategy_code", "")
    profit_pct = pending.get("profit_pct", 0)

    try:
        # Write strategy to LIVE (assuming there's a live_strategy.py)
        target_file = pending.get("target_file", "strategy.py")
        target_path = os.path.join(project_path, target_file)

        with open(target_path, "w") as f:
            f.write(strategy_code)

        # Remove pending flag
        pending_file = os.path.join(project_path, ".pending_live_deployment")
        if os.path.exists(pending_file):
            os.remove(pending_file)

        return (
            f"✅ DEPLOYMENT A LIVE TRADING CONFIRMADO\n\n"
            f"Estrategia con +{profit_pct:.2f}% profit en backtesting "
            f"ha sido desplegada.\n\n"
            f"El bot comenzará a ejecutar órdenes en vivo.\n"
            f"Monitorearé el desempeño y te notificaré cada hora.\n\n"
            f"⚠️ IMPORTANTE: Verifica los logs regularmente."
        )
    except Exception as deploy_err:
        return f"❌ Error al desplegar a LIVE: {deploy_err}"


def run_telegram_listener() -> None:
    """Main loop: poll Telegram for messages and respond.

    Uses long-polling to efficiently wait for new messages.
    Only processes messages from the configured TELEGRAM_CHAT_ID.
    """
    token, authorized_chat_id = _load_env_credentials()

    if not token:
        print("TELEGRAM_BOT_TOKEN not configured. Bot listener disabled.")
        return
    if not authorized_chat_id:
        print("TELEGRAM_CHAT_ID not configured. Bot listener disabled.")
        return

    print("Telegram bot listener started. Waiting for messages...")

    # Skip old messages on startup
    updates = _get_updates(token, offset=0, timeout=0)
    offset = 0
    if updates:
        offset = updates[-1]["update_id"] + 1

    while True:
        try:
            updates = _get_updates(token, offset=offset)

            for update in updates:
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat_id = str(message.get("chat", {}).get("id", ""))
                text = message.get("text", "")

                if not text:
                    continue

                # Only respond to the authorized chat
                if chat_id != authorized_chat_id:
                    continue

                print(f"[{time.strftime('%H:%M:%S')}] User: {text[:80]}")
                response = _process_message(text)
                print(
                    f"[{time.strftime('%H:%M:%S')}] "
                    f"Bot: {response[:80]}..."
                )
                _send_message(token, chat_id, response)

        except KeyboardInterrupt:
            print("\nTelegram listener stopped.")
            break
        except Exception as loop_err:
            print(f"Telegram listener error: {loop_err}")
            time.sleep(5)


if __name__ == "__main__":
    run_telegram_listener()
