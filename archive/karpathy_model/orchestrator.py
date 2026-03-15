import os
import subprocess
from google import genai

# Configuración del cliente y archivos
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
MODEL_ID = "gemini-2.5-flash-lite"
RESOURCE_FILE = "resource.md"  # Aquí se guarda la memoria del agente
TRAIN_FILE = "train.py"
INSTRUCTIONS_FILE = "program.md"

def run_orchestrator():
    print("--- INICIANDO CICLO DE AUTO RESEARCH (CON MEMORIA) ---")
    
    # 1. HARVEST: Leer código actual, instrucciones y la 'memoria' de experimentos previos
    if not os.path.exists(RESOURCE_FILE):
        with open(RESOURCE_FILE, "w") as f: f.write("# Log de Experimentos\n")

    with open(TRAIN_FILE, "r") as f: current_code = f.read()
    with open(INSTRUCTIONS_FILE, "r") as f: instructions = f.read()
    with open(RESOURCE_FILE, "r") as f: history = f.read()

    # 2. GENERATE: Gemini actúa como investigador analizando el pasado para crear el futuro
    prompt = f"""
    {instructions}
    
    HISTORIAL DE EXPERIMENTOS PREVIOS (Aprendizajes):
    {history}
    
    CÓDIGO ACTUAL DE '{TRAIN_FILE}':
    ```python
    {current_code}
    ```
    
    TAREA: Analiza los fallos y éxitos previos en el historial. 
    Propón un cambio en '{TRAIN_FILE}' para reducir el 'validation loss'.
    
    Responde en dos partes:
    1. Una breve explicación de tu hipótesis (por qué este cambio debería funcionar).
    2. El código completo de Python entre bloques ```python ```.
    """

    print("Gemini analizando historial y generando nueva variante...")
    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
    full_response = response.text

    # Extraer hipótesis y nuevo código de forma robusta
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

    # 3. DEPLOY: Aplicar cambios y ejecutar
    print(f"Hipótesis: {hypothesis}")
    with open(TRAIN_FILE, "w") as f:
        f.write(new_code)

    print("Ejecutando entrenamiento (5 min)...")
    try:
        # Se ejecuta con uv run para asegurar el entorno
        result = subprocess.run(["uv", "run", TRAIN_FILE], capture_output=True, text=True, timeout=300)
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = "Entrenamiento detenido por timeout (posible mejora o loop infinito)."
    except Exception as e:
        output = f"Error durante la ejecución: {e}"

    # GUARDAR APRENDIZAJE: Para que no esté "ciego" en la próxima carrera
    with open(RESOURCE_FILE, "a") as f:
        f.write(f"\n--- Nuevo Experimento ---\n")
        f.write(f"Hipótesis: {hypothesis}\n")
        # Guardamos los últimos 1000 caracteres de logs para capturar resultados y posibles errores
        f.write(f"Resultado (Logs): {output[-1000:]}\n") 
    
    print(f"Ciclo completado. Resultados guardados en {RESOURCE_FILE}.")

if __name__ == "__main__":
    run_orchestrator()
