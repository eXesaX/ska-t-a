from typing import List, Dict, Union

import aioredis

from pubsub.base import PubSubClient
from pubsub.serializer import Serializer


class RedisPubSubClient(PubSubClient):
    def __init__(self, url: str, serializer: Serializer):
        self.url = url
        self._client = aioredis.from_url(self.url)
        self._pubsub = self._client.pubsub()
        self._serializer = serializer

    async def publish(self, topic: str, message: Union[List, Dict]):
        await self._client.publish(topic, self._serializer.serialize(message))

    async def subscribe(self, topic: str):
        await self._pubsub.subscribe(topic)

    async def listen(self):
        async for data in self._pubsub.listen():
            if data['type'] == 'message':
                yield self._serializer.deserialize(data['data'])

