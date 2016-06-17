import redis
import xblock.runtime

from . import settings


class FieldData(xblock.runtime.KvsFieldData):
    def __init__(self):
        kvs = RedisKeyValueStore()
        super(FieldData, self).__init__(kvs)


class RedisKeyValueStore(xblock.runtime.KeyValueStore):
    """Redis-based KVS"""

    def __init__(self):
        self.client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    def get(self, key):
        value = self.client.get(key)
        if value is None:
            raise KeyError
        return value

    def has(self, key):
        return self.client.get(key) is not None

    def set(self, key, value):
        raise NotImplementedError
    def delete(self, key):
        raise NotImplementedError
