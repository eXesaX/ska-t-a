from pubsub.base import PubSubClient
from pubsub.redis import RedisPubSubClient
from pubsub.serializer import JsonSerializer


def get_pubsub_client() -> PubSubClient:
    return RedisPubSubClient("redis://localhost", JsonSerializer())