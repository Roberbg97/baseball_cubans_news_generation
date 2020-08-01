import json
from typing import Dict, List
import requests
from bs4 import Comment
from bs4 import BeautifulSoup
import datetime

PARSER = 'lxml'
try:
    import lxml
except ImportError:
    PARSER = 'html.parser'

nation = {
    'all': 0,
    'Aruba': 45,
    'Australia': 8,
    'Brasil': 47,
    'Canadá': 2,
    'Colombia': 14,
    'Cuba': 15,
    'Curacao': 16,
    'República Dominicana': 19,
    'Alemania': 23,
    'Honduras': 25,
    'Japón': 29,
    'Lituania': 117,
    'México': 30,
    'Holanda': 31,
    'Nicaragua': 32,
    'Panamá': 35,
    'Puerto Rico': 5,
    'Corea del Sur': 55,
    'Taiwán': 107,
    'Estados Unidos': 1,
    'Venezuela': 42
}

class Scrapper_for_country:
    def __init__(self, country = 'all'):
        self.country = country
        self._ss = requests.Session()
        self._ss.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Safari/537.36'
        self._base_url = 'https://www.baseball-reference.com'

    def get_players(self):

        session = self._ss

        base_url = self._base_url

        year = datetime.date.today().year

        r = session.get(base_url + '/bio/Cuba_born.shtml')
        bsObj = BeautifulSoup(r.text, PARSER)

        hitters = bsObj.find('table', {'id': 'bio_batting'}).tbody.find_all('tr')

        comments = bsObj.find_all(string=lambda text: isinstance(text, Comment))
        '''
        for i in comments:
            bs = BeautifulSoup(i, PARSER)
            h = bs.find('table', {'id': 'bio_batting'})
            if h is not None:
                print('hitters')
                hitters = h.tbody.findAll('tr')
                break
        '''

        for i in comments:
            bs = BeautifulSoup(i, PARSER)
            p = bs.find('table', {'id': 'bio_pitching'})
            if p is not None:
                #print('pitchers')
                pitchers = p.tbody.findAll('tr')
                break

        players = []
        for h in hitters:
            if 'class' not in h:
                name = h.find('td', {'data-stat': 'player'}).a.get_text()
                year_max = h.find('td', {'data-stat': 'year_max'}).get_text()
                year_max = int(year_max)
                if year_max == year:
                    players.append(name)

        for p in pitchers:
            if 'class' not in p:
                name = p.find('td', {'data-stat': 'player'}).a.get_text()
                year_max = p.find('td', {'data-stat': 'year_max'}).get_text()
                year_max = int(year_max)
                if year_max == year:
                    players.append(name)

        return players


s = Scrapper_for_country('Cuba')
#s._scrap()
#print(s.get_players())