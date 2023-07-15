import redis

from .producer import Producer
from .pubsubevent import PubSubEvent


class RedisProducer(Producer):
    def __init__(
        self, channel: str, host: str = "localhost", port: int = 6381, db: int = 0
    ):
        self.channel = channel
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)

    def produce(self, event: PubSubEvent) -> None:
        self.redis_client.publish(self.channel, event.to_json())

    def close(self):
        self.redis_client.close()
