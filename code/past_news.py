import os
try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from notice_generator.utils import get_yesterday_date as gyd
import datetime

class Renderer():
    def __init__(self, title, paragraphs, base_file='.'):
        self._title = title
        self._paragraphs = paragraphs
        self._base_file = base_file

    def render(self):

        past_news = json.load(open(os.path.join(MODULE, 'past_news.json'), 'r'))

        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        y = today - oneday

        name = 'new_' + str(y.day) + '-' + str(y.month) + '-' + str(y.year)

        past_news[name] = {
            'title': self._title,
            'paragraphs': self._paragraphs
        }

        for_templates = []

        for i in past_news.keys():
            for_templates.append((i, past_news[i]['title']))

        for_templates.pop()

        json.dump(past_news, open(os.path.join(MODULE, 'past_news.json'), 'w'))

        os.makedirs('past_news_pages', exist_ok=True)

        env = Environment(
            loader = FileSystemLoader(os.path.join(MODULE,'templates')),
            autoescape = select_autoescape(['html', 'xml'])
        )

        # Renderizando en las noticias pasadas

        principal_template = env.get_template('past_news_templates.html')

        principal_template = principal_template.render(title=self._title, paragraphs=self._paragraphs)

        with open(os.path.join(self._base_file, 'past_news_pages', name + '.html'), 'w') as h:
            h.write(principal_template)

        principal_template = env.get_template('principal_page_template.html')

        principal_template = principal_template.render(title=self._title, \
        paragraphs=self._paragraphs, past_news=for_templates)

        with open(os.path.join(self._base_file, 'index.html'), 'w') as h:
            h.write(principal_template)
            