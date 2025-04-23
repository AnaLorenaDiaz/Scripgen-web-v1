from openai_utils import generar_script
import traceback

# Sesiones simples (puedes mejorar con almacenamiento persistente si lo necesitas)
sesiones = {}

def procesar_mensaje_usuario(mensaje, session_id="default"):
    estado = sesiones.get(session_id, {"fase": 1})

    try:
        if estado["fase"] == 1:
            estado["descripcion"] = mensaje
            estado["fase"] = 2
            sesiones[session_id] = estado
            return (
                "📎 **Entendido**. Ahora necesito que me des la **RUTA COMPLETA DEL ARCHIVO EXCEL**, incluyendo el nombre del archivo.\n\n"
                "📌 *Ejemplo:*\n"
                "```\nC:\\Usuarios\\Ana\\Documentos\\Lista_clientes.xlsx\n```\n\n"
                "⚠️ Usa **dobles barras invertidas**: `\\` para que funcione correctamente. 😉"
            )

        elif estado["fase"] == 2:
            estado["ruta_archivo"] = mensaje
            estado["fase"] = 3
            sesiones[session_id] = estado
            return (
                "📄 Perfecto. ¿Cuál es el **nombre de la hoja** de Excel?\n\n"
                "📌 *Ejemplo:* `Hoja1`"
            )

        elif estado["fase"] == 3:
            estado["nombre_hoja"] = mensaje
            estado["fase"] = 4
            sesiones[session_id] = estado
            return (
                "📊 Genial. ¿Cuáles son las **columnas clave** a utilizar?\n\n"
                "📌 *Ejemplo:* `Nombre`, `Email`"
            )

        elif estado["fase"] == 4:
            estado["columnas"] = mensaje
            estado["fase"] = 5
            sesiones[session_id] = estado
            return (
                "🧠 Última pregunta: ¿Qué **acción** deseas realizar?\n\n"
                "📌 *Ejemplo:* `Eliminar duplicados`, `Filtrar por estado`, etc."
            )

        elif estado["fase"] == 5:
            estado["accion"] = mensaje
            sesiones[session_id] = {"fase": 1}  # Reinicia para nueva conversación

            prompt = (
                f"Eres un experto en PowerShell.\n\n"
                f"El usuario desea automatizar una tarea con un archivo Excel.\n\n"
                f"📄 Ruta del archivo: {estado['ruta_archivo']}\n"
                f"📄 Hoja: {estado['nombre_hoja']}\n"
                f"📄 Columnas: {estado['columnas']}\n"
                f"🎯 Acción a realizar: {estado['accion']}\n\n"
                f"Genera un script PowerShell bien comentado que cumpla con esta solicitud. "
                f"Incluye validación de existencia del archivo y explicaciones claras en comentarios."
            )

            script = generar_script(prompt)
            return (
                f"✅ ¡Script generado con éxito!\n\n"
                f"```powershell\n{script.strip()}\n```\n\n"
                f"📝 Este script automatiza: **{estado['accion']}**. Puedes copiarlo y probarlo en PowerShell."
            )

    except Exception as e:
        error_trace = traceback.format_exc()
        sesiones[session_id] = {"fase": 1}  # Reiniciar conversación tras fallo
        return (
            f"❌ Ocurrió un error inesperado: {str(e)}\n\n"
            f"🛠️ Detalles técnicos:\n```\n{error_trace}\n```"
        )

    # Fallback en caso de estado no esperado
    sesiones[session_id] = {"fase": 1}
    return "🔄 Algo salió mal. Reiniciando conversación. ¿Qué deseas automatizar con PowerShell?"
