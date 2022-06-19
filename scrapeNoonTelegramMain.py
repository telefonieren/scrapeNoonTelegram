import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.noon.com/uae-en/electronics-and-mobiles/mobiles-and-accessories/mobiles-20905/'

HEADERS ={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

req = requests.get(URL, HEADERS)

src = req.text
soup = BeautifulSoup(src, 'lxml')

page_number = soup.find(class_='next')