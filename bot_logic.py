from openai_utils import generar_script

# Sesiones simples por usuario
sesiones = {}

def procesar_mensaje_usuario(mensaje, session_id="default"):
    estado = sesiones.get(session_id, {"fase": 1})

    if estado["fase"] == 1:
        estado["descripcion"] = mensaje
        estado["fase"] = 2
        sesiones[session_id] = estado
        return (
            "\U0001F4CE **Entendido**. Ahora necesito que me des la *RUTA COMPLETA DEL ARCHIVO EXCEL*, incluyendo el nombre del archivo.\n\n"
            "\U0001F4CC *Ejemplo:*\n"
            "```
C:\\Usuarios\\Documentos\\Lista_clientes.xlsx
```
\n"
            "\u26A0\ufe0f Aseg\u00farate de escribirla correctamente para que el script funcione. \U0001F609"
        )

    elif estado["fase"] == 2:
        estado["ruta_archivo"] = mensaje
        estado["fase"] = 3
        sesiones[session_id] = estado
        return (
            "\U0001F4C4 Perfecto. ¿Cuál es el *NOMBRE de la HOJA* de Excel?\n\n"
            "\U0001F4CC *Ejemplo:* `Hoja1`"
        )

    elif estado["fase"] == 3:
        estado["nombre_hoja"] = mensaje
        estado["fase"] = 4
        sesiones[session_id] = estado
        return (
            "\U0001F4CA Genial. ¿Cuáles son las **columnas clave** a utilizar?\n\n"
            "\U0001F4CC *Ejemplo:* `Nombre`, `Email`"
        )

    elif estado["fase"] == 4:
        estado["columnas"] = mensaje
        estado["fase"] = 5
        sesiones[session_id] = estado
        return (
            "🧐 Última pregunta: ¿Qué *acción* deseas realizar?\n\n"
            "\U0001F4CC *Ejemplo:* `Eliminar duplicados`, `Filtrar por estado`, etc."
        )

    elif estado["fase"] == 5:
        estado["accion"] = mensaje
        sesiones[session_id] = estado

        prompt = (
            f"Eres un experto en PowerShell.\n\n"
            f"El usuario desea automatizar una tarea con un archivo Excel.\n\n"
            f"\U0001F4C4 Ruta del archivo: {estado['ruta_archivo']}\n"
            f"\U0001F4C4 Hoja: {estado['nombre_hoja']}\n"
            f"\U0001F4C4 Columnas: {estado['columnas']}\n"
            f"🎯 Acción a realizar: {estado['accion']}\n\n"
            f"Genera un script PowerShell bien comentado que cumpla con esta solicitud. "
            f"Incluye validación de existencia del archivo y explicaciones claras en comentarios."
        )

        try:
            respuesta_completa = generar_script(prompt)
            partes = respuesta_completa.split("```powershell")
            script = partes[1].split("```", 1)[0].strip() if len(partes) > 1 else respuesta_completa
            explicacion = respuesta_completa.replace(script, "").replace("```powershell", "").replace("```", "").strip()

            sesiones[session_id] = {
                "fase": 6,
                "explicacion": explicacion
            }

            return f"\u2705 \u00a1Script generado con éxito!\n\n```powershell\n{script}\n```"

        except Exception as e:
            sesiones[session_id] = {"fase": 1}
            return f"\u274c Ocurrió un error al generar el script: {str(e)}"

    elif estado["fase"] == 6:
        explicacion = estado.get("explicacion", "")
        sesiones[session_id] = {"fase": 1}
        return f"\U0001F4D8 Aquí tienes la explicación del script:\n\n{explicacion}"

    else:
        sesiones[session_id] = {"fase": 1}
        return "\U0001F501 Algo salió mal. Reiniciando conversación. ¿Qué deseas automatizar con PowerShell?"
