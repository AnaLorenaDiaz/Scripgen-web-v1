from aiohttp import web
from bot_logic import procesar_mensaje_usuario
import os
import traceback

# Ruta del endpoint principal
async def handle_post(request):
    try:
        data = await request.json()
        mensaje_usuario = data.get("text", "")
        session_id = data.get("session_id", "default")  # puedes adaptar esto a futuro
        respuesta = procesar_mensaje_usuario(mensaje_usuario, session_id)
        return web.json_response({"respuesta": respuesta})
    except Exception as e:
        error_trace = traceback.format_exc()
        return web.json_response({
            "error": str(e),
            "trace": error_trace
        }, status=500)

# Configura la app y las rutas
app = web.Application()
app.add_routes([web.post('/api/messages', handle_post)])

# Ejecuta el servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, port=port)
