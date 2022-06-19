import csv
import time
import requests
from bs4 import BeautifulSoup
import lxml

TARGET_DISCOUNT = 70

URL = 'https://www.noon.com/uae-en/electronics-and-mobiles/mobiles-and-accessories/mobiles-20905/'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

req = requests.get(URL, HEADERS)
src = req.text
soup = BeautifulSoup(src, 'lxml')

page_number = soup.find(class_='next').find_previous(class_='pageLink')  # Detecting number of pages
file_name = soup.find(class_='sc-2740ed02-1 pBrbb').text.strip() + '.csv'  # Initializing the filename for each category

with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
    goods_writer = csv.writer(csvfile)

    number_of_goods = 1

    for page in range(1, int(page_number.text) + 1):
        time.sleep(2)
        req = requests.get(URL + f'?page={page}')
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        print(f'****** Goods on the page {page} *********')

        goods = soup.find_all(class_='discount')
        for good in goods:

            good_discount = good.text.replace('%','').replace(' ','').replace('Off','').strip()
            if int(good_discount) > TARGET_DISCOUNT:
                old_price = good.find_previous(class_='oldPrice').text.strip()
                discounted_price = 'AED ' + good.find_previous(class_='currency').find_next('strong').text
                good_link = good.find_previous('a', href=True)
                discount_good_name = good.find_previous(class_="sc-d3293424-11 iOSKQc")
                print(f'{number_of_goods}. {discount_good_name.text.strip()} --->  {good.text.strip()}  WAS: {old_price} | NOW: {discounted_price}')
                number_of_goods += 1
                goods_writer.writerow([discount_good_name.text.strip()[:-2], good.text.strip(), old_price, discounted_price, 'noon.com'+good_link['href']])

csvfile.close()
