from abc import abstractmethod, ABCMeta


class LogListener(metaclass=ABCMeta):
    @abstractmethod
    def notify(self, data): pass
