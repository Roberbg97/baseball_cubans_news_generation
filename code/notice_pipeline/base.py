import abc


class Scrapper(metaclass=abc.ABCMeta):
    __slots__ = tuple(['_data'])
    def __init__(self):
        self._data=None

    @abc.abstractmethod
    def _scrap(self):
        raise NotImplementedError

    def scrap(self):
        self._data = self._scrap()
        return self._data

    @property
    def data(self):
        if self._data is not None:
            return self._data
        return self.scrap()

