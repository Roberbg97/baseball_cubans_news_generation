from base_algorithms_flow import *
from game_players_details_new import flow as scrapper_flow
from create_structured_data import get_outstandings, sort_for_outstandings
from create_structured_data import flow as flow_new_generation

class Scrapper_BR(Scrapper):
    def __init__(self):
        super().__init__()

    def scraping(self):
        return scrapper_flow()

class Outstandings_LR(Outstandings):
    def __init__(self):
        super().__init__()

    def get_sorted_outstandings(self):
        data = get_outstandings()
        return sort_for_outstandings(data)

class New_Templates(New):
    def __init__(self, player_details, sorted_for_outstandings):
        super().__init__(player_details, sorted_for_outstandings)

    def get_text(self):
        return flow_new_generation(self.player_details, self.sorted_for_outstandings)
