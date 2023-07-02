import abc


class Producer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def produce(self, *args, **kwargs) -> None:
        """Abstract method to handle incoming messages from the pub-sub system."""
        pass

    @abc.abstractmethod
    def close(self, *args, **kwargs) -> None:
        """Abstract method to close connections."""
        pass
