from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests
import db
import utils

url = 'https://pchome.megatime.com.tw/group/mkt4/cidA202.html'
req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, 'html.parser')
print(soup)