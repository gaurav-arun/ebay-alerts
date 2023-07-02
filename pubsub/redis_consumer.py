from .consumer import Consumer
import redis
from event import Event


class RedisConsumer(Consumer):
    def __init__(self, channel: str, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.channel = channel
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe(self.channel)

    def consume(self) -> Event:
        # TODO: Add sample message
        # TODO: Add exception handling
        # TODO: Add logging
        # TODO: Add type hints
        # TODO: Add docstrings
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                yield Event.from_json(message['data'])

    def close(self):
        self.pubsub.close()
        self.redis_client.close()
