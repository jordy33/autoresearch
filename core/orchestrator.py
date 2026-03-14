import os
import sys
import json
import subprocess
import time
from google import genai

def run_project(project_dir):
    config_path = os.path.join(project_dir, "config.json")
    if not os.path.exists(config_path):
        print(f"Skipping {project_dir}: config.json not found")
        return

    lock_file = os.path.join(project_dir, ".lock")
    if os.path.exists(lock_file):
        print(f"Skipping {project_dir}: .lock file exists (project is currently running)")
        return

    # Create lock file
    try:
        with open(lock_file, "w") as f:
            f.write(str(time.time()))
    except IOError:
        print(f"Failed to create lock file for {project_dir}")
        return

    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        project_name = config.get("project_name", "Unknown Project")
        target_file = config["experiment"]["target_file"]
        test_method = config["experiment"]["test_method"]
        model_id = config["agent_settings"].get("model", "gemini-2.5-pro")
        
        # Paths within the project directory
        target_path = os.path.join(project_dir, target_file)
        program_path = os.path.join(project_dir, "program.md")
        resource_path = os.path.join(project_dir, "resource.md")

        print(f"--- INICIANDO CICLO DE AUTO RESEARCH: {project_name} ---")

        # 1. HARVEST
        if not os.path.exists(resource_path):
            with open(resource_path, "w") as f: f.write("# Log de Experimentos\n")

        if not os.path.exists(target_path):
            print(f"Error: Target file {target_path} not found.")
            return

        with open(target_path, "r") as f: current_code = f.read()
        
        instructions = ""
        if os.path.exists(program_path):
            with open(program_path, "r") as f: instructions = f.read()
            
        with open(resource_path, "r") as f: history = f.read()

        # 2. GENERATE
        # Assumes GOOGLE_API_KEY is in env
        client = genai.Client() 
        prompt = f"""
        {instructions}
        
        HISTORIAL DE EXPERIMENTOS PREVIOS (Aprendizajes):
        {history}
        
        CÓDIGO ACTUAL DE '{target_file}':
        ```python
        {current_code}
        ```
        
        TAREA: Analiza los fallos y éxitos previos en el historial. 
        Propón un cambio en '{target_file}' para optimizar la métrica: {config['metric']['name']} ({config['metric']['goal']}).
        Señal de feedback a buscar: {config['metric']['feedback_signal']}
        
        Responde en dos partes:
        1. Una breve explicación de tu hipótesis (por qué este cambio debería funcionar).
        2. El código completo entre bloques ```python ```.
        """

        print(f"Gemini ({model_id}) analizando historial y generando nueva variante...")
        response = client.models.generate_content(model=model_id, contents=prompt)
        full_response = response.text

        try:
            if "```python" in full_response:
                parts = full_response.split("```python")
                hypothesis = parts[0].strip()
                new_code = parts[1].split("```")[0].strip()
            else:
                print("Error: Gemini no devolvió el formato de código esperado (faltan bloques ```python).")
                return
        except Exception as e:
            print(f"Error al procesar la respuesta de Gemini: {e}")
            return

        # 3. DEPLOY
        print(f"Hipótesis: {hypothesis}")
        with open(target_path, "w") as f:
            f.write(new_code)

        print(f"Ejecutando test: {test_method}...")
        try:
            # Ejecutar en el directorio del proyecto
            result = subprocess.run(test_method.split(), capture_output=True, text=True, timeout=config["experiment"].get("duration_minutes", 10) * 60, cwd=project_dir)
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "Entrenamiento detenido por timeout (posible mejora o loop infinito)."
        except Exception as e:
            output = f"Error durante la ejecución: {e}"

        # GUARDAR APRENDIZAJE
        with open(resource_path, "a") as f:
            f.write(f"\n--- Nuevo Experimento ---\n")
            f.write(f"Hipótesis: {hypothesis}\n")
            f.write(f"Resultado (Logs): {output[-1000:]}\n") 
        
        print(f"Ciclo completado para {project_name}. Resultados guardados en {resource_path}.")

        # Escribir la marca de tiempo de última ejecución para el daemon
        last_run_file = os.path.join(project_dir, ".last_run")
        with open(last_run_file, "w") as f:
            f.write(str(time.time()))

    finally:
        # Liberar el lock sin importar si hubo error o no
        if os.path.exists(lock_file):
            os.remove(lock_file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_project(sys.argv[1])
    else:
        projects_dir = "projects"
        if os.path.exists(projects_dir):
            for p in os.listdir(projects_dir):
                p_path = os.path.join(projects_dir, p)
                if os.path.isdir(p_path):
                    run_project(p_path)
