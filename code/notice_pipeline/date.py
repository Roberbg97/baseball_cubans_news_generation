import json
from typing import Dict, List, Union
import requests
from bs4 import Comment
from bs4 import BeautifulSoup
import re

PARSER = 'lxml'
try:
    import lxml
except ImportError:
    PARSER = 'html.parser'

def _get_date():
    ss = requests.Session()
    base_url = 'https://baseball-reference.com'
    r = ss.get(base_url)
    bsObj = BeautifulSoup(r.text, PARSER)
    date = bsObj.find('div', {'id': 'scores'}).h2.a['href']
    return date.replace('/boxes/?date=', '')

print(_get_date())