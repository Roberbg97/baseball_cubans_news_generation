import os
try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

import json
from first_algorithms_flow import Outstandings_LR, New_Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape
from notice_pipeline.scrapper import Scrapper_BR
from past_news import Renderer

def config():

    cubans = json.load(open(os.path.join(MODULE, 'cubans.json'), 'r'))

    #s = Scrapper_BR()
    s = Scrapper_BR(cubans)

    #player_details = s.scraping()
    d = s._scrap()

    o = Outstandings_LR()

    sfo = o.get_sorted_outstandings(d['game_day_data'])

    #nt = New_Templates(player_details, sfo)
    nt = New_Templates(d['game_day_data'], sfo, d['all_games_details'])

    title, paragraphs = nt.get_text()

    r = Renderer(title, paragraphs)

    r.render()

    return nt.get_text()

'''
env = Environment(
    loader = FileSystemLoader(os.path.join(MODULE,'templates')),
    autoescape = select_autoescape(['html', 'xml'])
)

template = env.get_template('principal_page_template.html')

title, paragraphs = config()

template = template.render(title=title, paragraphs=paragraphs)

with open(os.path.join(MODULE,'..','index.html'), 'w') as h:
    h.write(template)
    h.close()
'''

title, paragraphs = config()