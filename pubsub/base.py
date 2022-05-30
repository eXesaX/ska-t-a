from typing import Any


class PubSubClient:
    def __init__(self, *args, **kwargs):
        pass

    async def publish(self, topic: str, message: Any):
        raise NotImplemented()

    async def subscribe(self, topic: str):
        raise NotImplemented()

    async def listen(self):
        raise NotImplemented()
