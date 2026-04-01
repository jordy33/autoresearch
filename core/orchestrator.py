"""Auto-research experiment orchestrator.

Manages the autonomous research loop for trading strategy optimization.
Uses Gemini AI to analyze experiment history, generate improved strategies,
deploy them, run backtests, and record results.
"""

import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from datetime import timezone
from typing import Optional

from google import genai


def send_telegram(
    text: str,
    token: Optional[str] = None,
    chat_id: Optional[str] = None,
) -> None:
    """Send a message via Telegram bot.

    Loads credentials from environment variables or .env file if not
    provided directly.

    Args:
        text: The message text to send.
        token: Telegram bot token. Falls back to TELEGRAM_BOT_TOKEN env.
        chat_id: Telegram chat ID. Falls back to TELEGRAM_CHAT_ID env.
    """
    if not token:
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not chat_id:
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

    if not token or not chat_id:
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode(
        {"chat_id": chat_id, "text": text}
    ).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req):
            pass
    except Exception as send_error:
        print(f"Error enviando Telegram: {send_error}")


def run_project(project_dir: str) -> None:
    """Run a single auto-research cycle for a project.

    Executes the full loop: harvest history, generate new strategy via
    Gemini, deploy to target file, run backtest, and save results.

    Args:
        project_dir: Path to the project directory containing config.json.
    """
    config_path = os.path.join(project_dir, "config.json")
    if not os.path.exists(config_path):
        print(f"Skipping {project_dir}: config.json not found")
        return

    lock_file = os.path.join(project_dir, ".lock")
    if os.path.exists(lock_file):
        print(
            f"Skipping {project_dir}: "
            ".lock file exists (project is currently running)"
        )
        return

    try:
        with open(lock_file, "w") as lock:
            lock.write(str(time.time()))
    except IOError as io_err:
        print(f"Failed to create lock file for {project_dir}: {io_err}")
        return

    try:
        _execute_cycle(project_dir, config_path)
    finally:
        if os.path.exists(lock_file):
            os.remove(lock_file)


def _execute_cycle(project_dir: str, config_path: str) -> None:
    """Execute the core research cycle (harvest, generate, deploy).

    Args:
        project_dir: Path to the project directory.
        config_path: Path to the project's config.json.
    """
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    project_name = config.get("project_name", "Unknown Project")
    target_file = config["experiment"]["target_file"]
    test_method = config["experiment"]["test_method"]
    model_id = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-lite")

    target_path = os.path.join(project_dir, target_file)
    program_path = os.path.join(project_dir, "program.md")
    resource_path = os.path.join(project_dir, "resource.md")

    print(f"--- INICIANDO CICLO DE AUTO RESEARCH: {project_name} ---")

    # 1. HARVEST
    if not os.path.exists(resource_path):
        with open(resource_path, "w") as resource:
            resource.write("# Log de Experimentos\n")

    if not os.path.exists(target_path):
        print(f"Error: Target file {target_path} not found.")
        return

    with open(target_path, "r") as target:
        current_code = target.read()

    instructions = ""
    if os.path.exists(program_path):
        with open(program_path, "r") as program:
            instructions = program.read()

    with open(resource_path, "r") as resource:
        history = resource.read()

    # 2. GENERATE
    client = genai.Client()
    prompt = (
        f"{instructions}\n\n"
        f"HISTORIAL DE EXPERIMENTOS PREVIOS (Aprendizajes):\n"
        f"{history}\n\n"
        f"CÓDIGO ACTUAL DE '{target_file}':\n"
        f"```python\n{current_code}\n```\n\n"
        f"TAREA: Analiza los fallos y éxitos previos en el historial. "
        f"Propón un cambio en '{target_file}' para optimizar la métrica: "
        f"{config['metric']['name']} ({config['metric']['goal']}).\n"
        f"Señal de feedback a buscar: "
        f"{config['metric']['feedback_signal']}\n\n"
        f"Responde en dos partes:\n"
        f"1. Una breve explicación de tu hipótesis "
        f"(por qué este cambio debería funcionar).\n"
        f"2. El código completo entre bloques ```python ```."
    )

    print(
        f"Gemini ({model_id}) analizando historial "
        "y generando nueva variante..."
    )
    response = client.models.generate_content(
        model=model_id, contents=prompt
    )
    full_response = response.text

    try:
        if "```python" not in full_response:
            print(
                "Error: Gemini no devolvió el formato de código "
                "esperado (faltan bloques ```python)."
            )
            return
        parts = full_response.split("```python")
        hypothesis = parts[0].strip()
        new_code = parts[1].split("```")[0].strip()
    except Exception as parse_err:
        print(f"Error al procesar la respuesta de Gemini: {parse_err}")
        return

    # 3. DEPLOY
    print(f"Hipótesis: {hypothesis}")
    with open(target_path, "w") as target:
        target.write(new_code)

    output = _run_test(test_method, config, project_dir)

    # GUARDAR APRENDIZAJE
    timestamp_utc = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )
    with open(resource_path, "a") as resource:
        resource.write(f"\n--- Nuevo Experimento ({timestamp_utc}) ---\n")
        resource.write(f"Hipótesis: {hypothesis}\n")
        resource.write(f"Resultado (Logs): {output[-1000:]}\n")

    print(
        f"Ciclo completado para {project_name}. "
        f"Resultados guardados en {resource_path}."
    )

    # NOTIFICATIONS
    _handle_notifications(
        output,
        project_name,
        project_dir,
        test_method,
        hypothesis,
        new_code,
        config,
    )

    last_run_file = os.path.join(project_dir, ".last_run")
    with open(last_run_file, "w") as last_run:
        last_run.write(str(time.time()))


def _run_test(
    test_method: str, config: dict, project_dir: str
) -> str:
    """Execute the backtest command and return its output.

    Args:
        test_method: Shell command to run the test.
        config: Project configuration dictionary.
        project_dir: Path to the project directory.

    Returns:
        Combined stdout and stderr output from the test.
    """
    print(f"Ejecutando test: {test_method}...")
    try:
        timeout_secs = (
            config["experiment"].get("duration_minutes", 10) * 60
        )
        result = subprocess.run(
            test_method.split(),
            capture_output=True,
            text=True,
            timeout=timeout_secs,
            cwd=project_dir,
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return (
            "Entrenamiento detenido por timeout "
            "(posible mejora o loop infinito)."
        )
    except Exception as exec_err:
        return f"Error durante la ejecución: {exec_err}"


def _handle_notifications(
    output: str,
    project_name: str,
    project_dir: str,
    test_method: str,
    hypothesis: str,
    new_code: str,
    config: dict,
) -> None:
    """Send Telegram notifications for critical errors, successes, or morning summaries.

    Args:
        output: Test execution output to check for errors.
        project_name: Name of the project for the notification.
        project_dir: Path to the project directory.
        test_method: Test command (used to detect dry_run mode).
        hypothesis: The current experiment hypothesis text.
        new_code: The new strategy code deployed.
        config: Project configuration dictionary.
    """
    is_critical = "Error" in output or "-100.00" in output
    profit_str = _extract_profit(output)
    profit_pct = float(profit_str) if profit_str else None

    if is_critical:
        send_telegram(
            f"🚨 ERROR CRÍTICO en {project_name}:\n{output[-500:]}"
        )
    elif profit_pct is not None and profit_pct > 10.0 and "dry_run" in test_method:
        # Positive backtest! Ask for LIVE deployment confirmation
        _create_pending_deployment(
            project_dir, new_code, profit_pct, config
        )
        send_telegram(
            f"🟢 BACKTEST POSITIVO en {project_name}!\n\n"
            f"Profit: +{profit_pct:.2f}%\n\n"
            f"Hipótesis:\n{hypothesis}\n\n"
            f"¿Queremos desplegar a LIVE trading?\n\n"
            f"Responde: `/confirm_live` para ejecutar"
        )
    elif current_hour == 8:
        _send_morning_summary(
            project_name, project_dir, test_method, hypothesis, output
        )


def _extract_profit(output: str) -> Optional[str]:
    """Extract PROFIT_LOSS_PCT value from test output.

    Args:
        output: Test execution output.

    Returns:
        Profit percentage string or None if not found.
    """
    for line in output.split("\n"):
        if "PROFIT_LOSS_PCT:" in line:
            try:
                return line.split("PROFIT_LOSS_PCT:")[-1].strip()
            except Exception:
                pass
    return None


def _create_pending_deployment(
    project_dir: str,
    strategy_code: str,
    profit_pct: float,
    config: dict,
) -> None:
    """Save pending LIVE deployment info for user confirmation.

    Args:
        project_dir: Path to the project directory.
        strategy_code: The strategy code to deploy.
        profit_pct: Profit percentage from backtest.
        config: Project configuration.
    """
    target_file = config["experiment"]["target_file"]
    pending_data = {
        "project_path": project_dir,
        "strategy_code": strategy_code,
        "profit_pct": profit_pct,
        "target_file": target_file,
        "timestamp_utc": datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        ),
    }

    pending_file = os.path.join(project_dir, ".pending_live_deployment")
    with open(pending_file, "w") as f:
        json.dump(pending_data, f, indent=2)


def _send_morning_summary(
    project_name: str,
    project_dir: str,
    test_method: str,
    hypothesis: str,
    output: str,
) -> None:
    """Send a daily morning summary if not already sent today.

    Args:
        project_name: Name of the project.
        project_dir: Path to the project directory.
        test_method: Test command (used to detect dry_run mode).
        hypothesis: The current experiment hypothesis text.
        output: Latest test output.
    """
    current_hour = datetime.now().hour
    if current_hour != 8:
        return

    summary_file = os.path.join(project_dir, ".last_summary")
    today_str = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(summary_file):
        with open(summary_file, "r") as summary:
            if summary.read().strip() == today_str:
                return

    send_telegram(
        f"🌅 RESUMEN MATUTINO ({project_name})\n\n"
        f"Hipótesis de la noche:\n{hypothesis}\n\n"
        f"Último Resultado:\n{output[-200:]}"
    )
    with open(summary_file, "w") as summary:
        summary.write(today_str)


def main() -> None:
    """Entry point: run research cycles for one or all projects."""
    if len(sys.argv) > 1:
        run_project(sys.argv[1])
    else:
        projects_dir = "projects"
        if os.path.exists(projects_dir):
            for project in os.listdir(projects_dir):
                project_path = os.path.join(projects_dir, project)
                if os.path.isdir(project_path):
                    run_project(project_path)


if __name__ == "__main__":
    main()
