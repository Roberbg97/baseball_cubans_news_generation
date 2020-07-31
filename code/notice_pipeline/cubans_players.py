import json
from typing import Dict, List
import requests
from bs4 import Comment
from bs4 import BeautifulSoup

PARSER = 'lxml'
try:
    import lxml
except ImportError:
    PARSER = 'html.parser'

class Scrapper_for_country:
    def __init__(self, country = 'all'):
        self.country = country
        self.index = 0
        if country == 'Cuba':
            self.index = 15
        self._ss = requests.Session()
        self._ss.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Safari/537.36'
        self._base_url = 'http://espndeportes.espn.com/beisbol/mlb'

    def get_players(self):
        if self.country == 'all':
            return []

        players = self._scrap()
        for i in range(len(players)):
            last, name = players[i].split(', ')
            players[i] = name + ' ' + last
        return players

    def _scrap(self):
        
        session = self._ss
        
        base_url = self._base_url
        r = session.get(base_url + '/players?country=' + str(self.index))
        bsObj = BeautifulSoup(r.text, PARSER)

        players = bsObj.find('div', {'id': 'my-players-table'}).findAll('tr')[2:]

        filter_players = []

        for p in players:
            pl = p.td.a.get_text()
            filter_players.append(pl)

        return filter_players



#s = Scrapper_for_country()
#s._scrap()
#s.get_players()