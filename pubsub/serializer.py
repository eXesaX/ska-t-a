import json
from typing import Union, List, Dict


class Serializer:
    @staticmethod
    def serialize(obj: Union[List, Dict]) -> bytes:
        raise NotImplemented()

    @staticmethod
    def deserialize(data: bytes) -> Union[List, Dict]:
        raise NotImplemented()


class JsonSerializer(Serializer):
    @staticmethod
    def serialize(obj: Union[List, Dict]) -> bytes:
        return json.dumps(obj).encode('utf-8')

    @staticmethod
    def deserialize(data: bytes) -> Union[List, Dict]:
        return json.loads(data)

