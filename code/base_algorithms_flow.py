import abc

class Scrapper(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def scraping(self):
        raise NotImplementedError

class Outstandings(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_sorted_outstandings(self):
        raise NotImplementedError

class New(metaclass=abc.ABCMeta):
    def __init__(self, player_details, sorted_for_outstandings, games_details):
        self.player_details = player_details
        self.sorted_for_outstandings = sorted_for_outstandings
        self.games_details = games_details

    @abc.abstractmethod
    def get_text(self):
        raise NotImplementedError