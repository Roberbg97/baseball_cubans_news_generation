from first_algorithms_flow import Scrapper_BR, Outstandings_LR, New_Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape

def config():
    s = Scrapper_BR()

    player_details = s.scraping()

    o = Outstandings_LR()

    sfo = o.get_sorted_outstandings()

    nt = New_Templates(player_details, sfo)

    return nt.get_text()

env = Environment(
    loader = FileSystemLoader('./templates'),
    autoescape = select_autoescape(['html', 'xml'])
)

template = env.get_template('principal_page_template.html')

title, text = config()

template = template.render(title=title, text=text)

with open('../index.html', 'w') as h:
    h.write(template)
    h.close()
