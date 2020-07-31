import json
from importlib import import_module
from configparser import ConfigParser
#from first_algorithms_flow import Outstandings_LR, New_Templates
#from jinja2 import Environment, FileSystemLoader, select_autoescape
#from notice_pipeline.scrapper import Scrapper_BR
#from past_news import Renderer
import os
try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""


def config():

    #cubans = json.load(open(os.path.join(MODULE, 'cubans.json'), 'r'))

    parser = ConfigParser()
    parser.read(os.path.join(MODULE, 'config.ini'))

    scraping_players_module = parser.get('country', 'module')
    scraping_players_class = parser.get('country', 'class')
    scraping_players_country = parser.get('country', 'country')

    scraping_module = parser.get('scraping', 'module')
    scraping_class = parser.get('scraping', 'class')

    clasification_module = parser.get('clasification', 'module')
    clasification_class = parser.get('clasification', 'class')

    gen_module = parser.get('generation', 'module')
    gen_class = parser.get('generation', 'class')

    render_module = parser.get('render', 'module')
    render_class = parser.get('render', 'class')

    module = import_module(scraping_players_module)
    class_ = getattr(module, scraping_players_class)
    c = class_(scraping_players_country)

    cubans = c.get_players()
    print(cubans)

    module = import_module(scraping_module)
    class_ = getattr(module, scraping_class)
    s = class_(cubans)

    #s = Scrapper_BR(cubans)

    #player_details = s.scraping()
    d = s._scrap()


    module = import_module(clasification_module)
    class_ = getattr(module, clasification_class)
    o = class_()
    #o = Outstandings_LR()

    sfo = o.get_sorted_outstandings(d['game_day_data'])


    module = import_module(gen_module)
    class_ = getattr(module, gen_class)
    nt = class_(d['game_day_data'], sfo, d['all_games_details'])

    #nt = New_Templates(player_details, sfo)
    #nt = New_Templates(d['game_day_data'], sfo, d['all_games_details'])

    title, paragraphs = nt.get_text()

    module = import_module(render_module)
    class_ = getattr(module, render_class)
    r = class_(title, paragraphs)
    #r = Renderer(title, paragraphs)

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

config()