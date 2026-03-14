import os
from google import genai

# Inicializa el cliente con la nueva librería
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def test_connection():
    # El método cambia a client.models.generate_content
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", 
        contents="Confirmación: ¿Estás listo para operar como orquestador con la nueva librería?"
    )
    print("Respuesta de Gemini:", response.text)

if __name__ == "__main__":
    test_connection()