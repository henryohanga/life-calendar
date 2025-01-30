import contextvars
from uuid import uuid4

request_id_ctx = contextvars.ContextVar("request_id", default=None)


def get_request_id() -> str:
    """Get the current request ID or generate a new one"""
    request_id = request_id_ctx.get()
    if request_id is None:
        request_id = str(uuid4())
        request_id_ctx.set(request_id)
    return request_id
