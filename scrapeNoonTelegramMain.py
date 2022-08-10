import time
import requests
from bs4 import BeautifulSoup
import json

TARGET_DISCOUNT = 74

URLS = [
    'https://www.noon.com/uae-en/fashion/fashion-men/',
    'https://www.noon.com/uae-en/fashion/fashion-women/',
    'https://www.noon.com/uae-en/home-and-kitchen/',
    'https://www.noon.com/uae-en/electronics-and-mobiles/',
    'https://www.noon.com/uae-en/beauty-and-health/',
    'https://www.noon.com/uae-en/beauty-and-health/beauty/fragrance/',
    'https://www.noon.com/uae-en/toys-and-games/',
    'https://www.noon.com/uae-en/sports-and-outdoors/'
]

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0'
                  ' Safari/537.36'
}


def get_goods_to_json(URL):
    req = requests.get(URL)
    src = req.text

    soup = BeautifulSoup(src, 'lxml')
    file_string = URL.split('/')[:-1]
    print(file_string[-1])
    page_number = int(soup.find(class_='next').find_previous(class_='pageLink').text)  # Detecting number of pages
    file_name = file_string[-1] + '.json'  # Initializing the filename for each category
    result_data = []

    number_of_goods = 1
    if page_number > 49:
        page_number = 49
    for page in range(1, page_number):
        try:
            time.sleep(0.1)

            req = requests.get(URL + f'?limit=50&page={page}&sort[by]=popularity&sort[dir]=desc', HEADERS)
            src = req.text

            soup = BeautifulSoup(src, 'lxml')
            print(
                f'****** Finding goods with {TARGET_DISCOUNT}% and more discount on the page {page} out of {page_number} '
                f'pages *********')

            goods = soup.find_all(class_='discount')

            for good in goods:

                good_discount = good.text.replace('%', '').replace(' ', '').replace('Off', '').strip()

                if int(good_discount) > TARGET_DISCOUNT:
                    old_price = good.find_previous(class_='oldPrice').text.strip()
                    discounted_price = 'AED ' + good.find_previous(class_='currency').find_next('strong').text
                    good_link = good.find_previous('a', href=True)

                    discount_good_name = good.find_previous('div', attrs={'data-qa': 'product-name'})

                    print(
                        f'{number_of_goods}. {discount_good_name.text.strip()} --->  {good.text.strip()}  WAS: {old_price} '
                        f'| NOW: {discounted_price}')
                    number_of_goods += 1

                    result_data.append(
                        {
                            'title': discount_good_name.text.strip()[:-2],
                            'discount': good.text.strip(),
                            'old_price': old_price,
                            'new_price': discounted_price,
                            'link': 'noon.com' + good_link['href']
                        }
                    )

            print(f'So far, found {number_of_goods - 1} discounted products')
        except:
            print("failed to open page")
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    for URL in URLS:
        get_goods_to_json(URL)

    with open('log.txt', 'w') as file:
        file.write('done')
    file.close()


if __name__ == '__main__':
    main()
