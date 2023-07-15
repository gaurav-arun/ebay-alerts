import abc


class Consumer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def consume(self, *args, **kwargs):
        """Abstract method to handle incoming messages from the pub-sub system."""

    @abc.abstractmethod
    def close(self, *args, **kwargs):
        """Abstract method to close connections."""
