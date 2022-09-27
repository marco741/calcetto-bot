from telethon import events

def last_handler_decorator(handler):
    """Decorator that blocks the propagation of a telethon message/cb_query event"""

    async def wrapper(*args, **kwargs):
        await handler(*args, **kwargs)
        raise events.StopPropagation
    return wrapper