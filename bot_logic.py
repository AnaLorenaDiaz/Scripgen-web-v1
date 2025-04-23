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
             "📎 **Entendido**. Ahora necesito que me des la *RUTA COMPLETA DEL ARCHIVO EXCEL*, incluyendo el nombre del archivo.\n\n"
             "📌 *Ejemplo:*\n"
             "```\n"
             "C:\\Usuarios\\Documentos\\Lista_clientes.xlsx\n"
             "```\n\n"
             "```\nC:\\Usuarios\\Documentos\\Lista_clientes.xlsx\n```\n\n"
             "⚠️ Asegúrate de escribirla correctamente para que el script funcione. 😉"
         )
 
     elif estado["fase"] == 2:
         estado["ruta_archivo"] = mensaje
         estado["fase"] = 3
         sesiones[session_id] = estado
         return (
             "📄 Perfecto. ¿Cuál es el *NOMBRE de la HOJA* de Excel?\n\n"
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
             "🧠 Última pregunta: ¿Qué *acción* deseas realizar?\n\n"
             "📌 *Ejemplo:* `Eliminar duplicados`, `Filtrar por estado`, etc."
         )
 
     elif estado["fase"] == 5:
         estado["accion"] = mensaje
         sesiones[session_id] = {"fase": 1}  # Reinicio de conversación
         sesiones[session_id] = estado  # No reiniciamos aún
 
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
 
         try:
             script = generar_script(prompt)
             return (
                 f"✅ ¡Script generado con éxito!\n\n"
                 f"```powershell\n{script.strip()}\n```\n\n"
                 f"📝 Este script automatiza: **{estado['accion']}**. Puedes copiarlo y probarlo en PowerShell."
             )
             respuesta_completa = generar_script(prompt)
 
             # Dividimos la respuesta: antes y después de la palabra "```powershell"
             partes = respuesta_completa.split("```powershell")
             script = partes[1].split("```")[0].strip() if len(partes) > 1 else respuesta_completa
             explicacion = respuesta_completa.replace(script, "").replace("```powershell", "").replace("```", "").strip()
 
             # Guardamos la explicación para el siguiente mensaje
             sesiones[session_id] = {
                 "fase": 6,
                 "explicacion": explicacion
             }
 
             return f"✅ ¡Script generado con éxito!\n\n```powershell\n{script}\n```"
 
         except Exception as e:
             sesiones[session_id] = {"fase": 1}
             return f"❌ Ocurrió un error al generar el script: {str(e)}"
 
     elif estado["fase"] == 6:
         # En esta fase solo mostramos la explicación guardada y reiniciamos
         explicacion = estado.get("explicacion", "")
         sesiones[session_id] = {"fase": 1}
         return f"📘 Aquí tienes la explicación del script:\n\n{explicacion}"
 
     else:
         sesiones[session_id] = {"fase": 1}
         return "🔄 Algo salió mal. Reiniciando conversación. ¿Qué deseas automatizar con PowerShell?"
