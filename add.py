from bs4 import BeautifulSoup
import requests
from lxml import etree
import json


def get_exchange():
    # Get exchange rate USD/PLN from NBP site
    page = requests.get('https://www.nbp.pl/home.aspx?f=/kursy/kursya.html')
    soup = BeautifulSoup(page.content, features="lxml")
    dom = etree.HTML(str(soup))
    return float(dom.xpath('//tr[2]/td[3][@class="right"]')[0].text.replace(',', '.'))


def get_settings(setting):
    # Gets setting from settings.json
    settings_file = open("input/settings.json")
    settings = json.load(settings_file)
    return settings[setting]
