# ScriptGen Agent

Agente conversacional que genera scripts de PowerShell personalizados a partir de instrucciones en lenguaje natural. Utiliza Azure OpenAI y puede integrarse con Microsoft Teams.

el bash se refiere a la ejecución en POWERSHELL (línea por línea)


---

## 📌 Características

- 🤖 Interacción guiada paso a paso
- 📝 Solicita al usuario qué desea automatizar
- 📂 Pide el archivo Excel y su ruta
- 🧾 Genera scripts PowerShell comentados
- 🧠 Se conecta a Azure OpenAI (GPT-4o)
- ⚙️ Preparado para desplegar en Azure App Service
- 💬 Integrable con Microsoft Teams (via Azure Bot)

---

## ⚙️ Requisitos previos

- Python 3.10 o superior
- Cuenta activa de Azure con acceso a Azure OpenAI
- Clave de API y Endpoint de un recurso OpenAI con modelo desplegado (`gpt-4`, `gpt-4o`)

---

## Estructura del proyecto

scriptgen-agent/
│
├── app.py               # Servidor principal con aiohttp
├── bot_logic.py         # Lógica de conversación por fases
├── openai_utils.py      # Función para conectar con Azure OpenAI
├── .env                 # Claves de entorno (⚠️ No compartas ni subas este archivo a GitHub)
├── requirements.txt     # Lista de librerías necesarias
└── README.md            # Este archivo ✨

## 🛠️ Configuración del entorno

### 📦 PRIMERA VEZ

                ```bash
                cd "C:\Users\AnaDíaz\Documents\PROYECTOS\scriptgen-agent"
                python -m venv env             # 🔧 Esto crea el entorno virtual (solo una vez)
                .\env\Scripts\activate         # 🚀 Activa el entorno virtual
                pip install -r requirements.txt # 📦 Instala las dependencias necesarias (solo una vez)
                python app.py                  # ▶️ Inicia la aplicación
                ```

### 📦 OTRAS VECES

                ```bash
                cd "C:\Users\AnaDíaz\Documents\PROYECTOS\scriptgen-agent"
                .\env\Scripts\activate         # 🚀 Activa el entorno virtual
                python app.py                  # ▶️ Inicia la aplicación
                ```

### Pruebas con Postman

1) Asegurate que se haya realizado los pasos de "Configuración del entorno - OTRAS VECES"
2) Abre Postman > New > HTTP
3) Cambia el GET por POST
4) URL: <http://localhost:8000/api/messages>
5) Haz clic en BODY > raw > A la derecha de GraphQL, cámbialo a JSON
6) Pega este contenido

```json
{
  "text": "Quiero crear un script que elimine los registros duplicados según el correo"
}

{
  "text": "C:\\Users\\AnaDíaz\\Documents\\PROYECTOS\\scriptgen-agent\\Lista_clientes.xlsx"
}

{
  "text": "Clientes2023"
}

{
  "text": "Nombre, Email"
}

{
  "text": "Eliminar duplicados basados en la columna Email"
}
```
