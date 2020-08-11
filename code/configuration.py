from notice_pipeline import *
import json
import datetime
import os
try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

class Armandobot(Configuration):
    __slots__ = ()

    def _instanciate_country(self):
        return Scrapper_for_country(self._config.get('country', 'country'))

    def _instanciate_scraping(self):
        return Scrapper_BR([])

    def _instanciate_clasification(self):
        return Outstandings_LR()

    def _instanciate_generation(self, player_details, sorted_for_outstandings, games_details, players_teams):
        return New_Templates(player_details, sorted_for_outstandings, games_details, players_teams)

    def _run(self, *args, **kwargs):
        res = kwargs.pop('pipeline_result')
        res["author"] = "Armanbot"
        try:
            past_news = json.load(open('past_news.json'))
        except Exception as e:
            print(e)
            past_news = {}

        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        y = today - oneday

        day = str(y.day)
        month = str(y.month)
        year = str(y.year)

        if len(day) == 1:
            day = '0' + day

        if len(month) == 1:
            month = '0' + month

        name = year + '-' + month + '-' + day

        past_news[name] = res

        json.dump(past_news, open('past_news.json', 'w'), indent=2)

        #r.render()

        return (res['title'], res['paragraphs'], res['summary'])

if __name__ == "__main__":
    cfg = Armandobot(config_file=os.path.join(MODULE, 'config.ini'))
    cfg.run()