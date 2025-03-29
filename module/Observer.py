from abc import ABC, abstractmethod

class Subject(ABC):

    @abstractmethod
    def registerObserver(self, observer):
        pass

    @abstractmethod
    def _notifyObservers(self):
        pass


class Observer(ABC):

    @abstractmethod
    def update(self, data):
        pass