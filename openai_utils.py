import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración para Azure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2024-02-15-preview"

deployment_name = os.getenv("DEPLOYMENT_NAME")

def generar_script(prompt_usuario):
    try:
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": "Eres un experto en PowerShell que genera scripts eficientes para archivos Excel. Siempre responde en español y con comentarios claros en el código."
                },
                {
                    "role": "user",
                    "content": prompt_usuario
                }
            ],
            temperature=0.4,
            max_tokens=1000
        )
        return response.choices[0].message["content"]

    except Exception as e:
        return f"⚠️ Error al generar el script: {str(e)}"
