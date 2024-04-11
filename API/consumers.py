import socketio
import os

from urllib.parse import parse_qs

WS_MESSAGE_QUEUE=os.environ.get("WS_MESSAGE_QUEUE")

mgr = socketio.AsyncRedisManager(WS_MESSAGE_QUEUE)
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[],
    client_manager=mgr,
    logger=True,
    engineio_logger=True,
)

external_sio = socketio.AsyncRedisManager(WS_MESSAGE_QUEUE, write_only=True)
sio_app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    await sio.emit("test", to=sid)


# @sio.event
# async def disconnect(sid):
#     try:
#         user_session_data = await redis_cache.redis_cache.hgetall(sid)
#         await sio.disconnect(sid)
#         await redis_cache.redis_cache.delete(sid)
#         print(sid, "disconnected")
#     except KeyError:
#         await sio.disconnect(sid)
#         print(sid, "disconnected")
