import json
import pickle
import msgpack


class Serializer:
    """Class for comparing the speed of serialization, serialization with deserialization"""

    def serialize_json(self, data: str) -> None:
        serialized_data = json.dumps(data)
        return serialized_data

    def serialize_pickle(self, data: str) -> str:
        serialized_data = pickle.dumps(data)
        return serialized_data

    def serialize_msgpack(self, data: str) -> str:
        serialized_data = msgpack.packb(data)
        return serialized_data

    def serialize_and_de_json(self, data: str) -> str:
        deserialized_data = json.loads(self.serialize_json(data))
        return deserialized_data

    def serialize_and_de_pickle(self, data: str) -> str:
        deserialized_data = pickle.loads(self.serialize_pickle(data))
        return deserialized_data

    def serialize_and_de_msgpack(self, data: str) -> str:
        deserialized_data = msgpack.unpackb(self.serialize_msgpack(data))
        return deserialized_data
