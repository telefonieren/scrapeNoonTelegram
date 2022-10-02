import time
import requests
from bs4 import BeautifulSoup
import json
import lxml
from fp.fp import FreeProxy

TARGET_DISCOUNT = 74

PROXY = {
    'http': 'http://147.75.88.45:10001',
    'https': 'http://147.75.88.45:10001',
}

URLS = [
    'https://www.noon.com/uae-en/beauty-and-health/',
    'https://www.noon.com/uae-en/beauty-and-health/beauty/fragrance/',
    'https://www.noon.com/uae-en/toys-and-games/',
    'https://www.noon.com/uae-en/sports-and-outdoors/'
]


# HEADERS = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
#               'application/signed-exchange;v=b3;q=0.9',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0'
#                   ' Safari/537.36'
# }


def collect_data(page, product_url):
    fashion_list = []
    number_of_goods = 1
    print(f'Processing {product_url}')
    print(f'Writing to ** {product_url.replace("/", "-")[28:-1]}.json ** file')
    for i in range(1, page + 1):
        cookies = {
            'visitor_id': '341f438b-7cfc-4a4f-87aa-e9d0ddd1d364',
            'x-available-ae': 'ecom-daily',
            '_gcl_au': '1.1.2048316385.1658574097',
            '_ga': 'GA1.2.1379022618.1658574097',
            '_scid': 'c91fa748-f381-4df8-a009-870eca0e8570',
            '__zlcmid': '1B6l60mt7QofUVG',
            '_sctr': '1|1660510800000',
            '_gid': 'GA1.2.1824498382.1660849712',
            'AKA_A2': 'A',
            'bm_mi': '046582BE43CD2B49104B496BC1594CC8~YAAQPzorF31iAoyCAQAA2+CsthBhInvIOl8kyMmgboycv4wCkQ/j3yJ/Jz/UMnXcTdPZ7O1el2BlaPK26BR5mQB36fyoA15YqcNFlbyT2ykp1maS/vFi2NmFdnItknOaldZW8VX5nlCFJZl9JCMmE79Oplupph7m8GwE1RNHd1s91chTLBSlXb8R/iCasGNxJsuspccxfsqUDvon9uts7UvkYZWjhhSCdPjJ6t5esrecX+UytFsKNE2lA+iMcZ2agBAJyRSYtIs1aR+5PHkQxP8URcBpHh7J89XtiA3/teKJrMULsbb9QaNg27U2PI8fQ90aLxPOpcuelOuH80G0M6BPZGA=~1',
            'nguest': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnJhV1FpT2lJeVlUSmlaalZqTWpGbU5EZzBNVFV6WVRsbE0yWmxNelF4TjJGaFpURTJZU0lzSW1saGRDSTZNVFkxT0RVM05EQTVPSDAuZkhhcTNCY05adHdzdEJOYmVrM3Q5cjZmQm5ZdnctQ2N6TXNkdGZmU2JnRSIsImlhdCI6MTY2MDkyMjE2M30.OztXSHorDq7UjpvzvKsPuqRf1SjophEbmVacF5HcNQQ',
            '_nsc': 'nsv1.public.eyJzdGlkIjoiNDlmZWM0NzgtNWQxMi00OGU0LTk2ZWUtODgzOGJiZmE5NmE0Iiwic2lkIjoiMmEyYmY1YzIxZjQ4NDE1M2E5ZTNmZTM0MTdhYWUxNmEiLCJpYXQiOjE2NjA5MjIxNjMsInZpZCI6IjM0MWY0MzhiLTdjZmMtNGE0Zi04N2FhLWU5ZDBkZGQxZDM2NCIsImhvbWVwYWdlIjp7fX02emdrY0NqUTFmQXdqWElNYXFVMEhMRys0dm1NYUNhZVJDcEsxREMzTHRzPQ.MQ',
            'ak_bmsc': 'D2BABE42B90EC55CC1E9300A794242C8~000000000000000000000000000000~YAAQPzorF61/AoyCAQAADhOvthDmHRWSOEp0Bf0K+JWTNF18RV5DhnXzPSHyxwe1N/0LwucBcvmhw0AnPNrHtkDtMnj/0SBLCM/X3u3jzDfHUvQjQTgmXJz4p/9re58ueHplsy4gLxW2JwiWG4vuoSFkHFbu0dcPxOEuAf/iO+uthptbPynVgKzmwrw33H+Mm5VfHSVTRh819xe0+rNX6A23XxQ2h9UOtnE0yhHmh5TwCp+pFxDX7KaOoLVcBLYDAKhuXirceSVplr3M4u3CzOmWUCgsTmp6Nrhlq9tcuS0Uw9MAvfZDmvhh+zJVcmBtWnj+jWipmWXn2V5B9nNYzos4KHKhCZrZpmkWfS50dNp307x4HAe/INjChsptKiUdfydOEw72YM9D/gvuihFWhd8HYOsLF4u75hlQdN31B+16LUHy0c+BNVssCKX1Wnzs4Z+Z',
            'bm_sv': 'F0717CB0273A61815258B7EC77A13C20~YAAQPzorF81iA4yCAQAANj/AthC1TA9vD1JBTYAUqokvPQtxPgVFrVCQ9NbLbu5sPNjYqOrNIIMy+KUaAJfwX/Qymk/FAj2XypqJBt+li7O2vZNaF5l4Yaf60l7oqcUBdIICBBSD6onDcdEF8qEfEC3qf7Nb3OyomEHrnCnlFuzdxdOhbSnE61gXgW/vC8TYltY2/Vq7fYBgdTjXwC2eUp/j8Fm0Uj95Io1BgTrOjZea8XHWNHw11fVcq/DRog==~1',
            'RT': '"z=1&dm=noon.com&si=b8437eea-94ad-4e36-8cac-b182d2efe0a9&ss=l70m62kl&sl=2&tt=1dtw&rl=1&ul=r76n&hd=r8d3"',
            '_etc': 'OpXYfOnXi1iVcEnm',
        }

        headers = {
            'authority': 'www.noon.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
            # Requests sorts cookies= alphabetically
            # 'cookie': 'visitor_id=341f438b-7cfc-4a4f-87aa-e9d0ddd1d364; x-available-ae=ecom-daily; _gcl_au=1.1.2048316385.1658574097; _ga=GA1.2.1379022618.1658574097; _scid=c91fa748-f381-4df8-a009-870eca0e8570; __zlcmid=1B6l60mt7QofUVG; _sctr=1|1660510800000; _gid=GA1.2.1824498382.1660849712; AKA_A2=A; bm_mi=046582BE43CD2B49104B496BC1594CC8~YAAQPzorF31iAoyCAQAA2+CsthBhInvIOl8kyMmgboycv4wCkQ/j3yJ/Jz/UMnXcTdPZ7O1el2BlaPK26BR5mQB36fyoA15YqcNFlbyT2ykp1maS/vFi2NmFdnItknOaldZW8VX5nlCFJZl9JCMmE79Oplupph7m8GwE1RNHd1s91chTLBSlXb8R/iCasGNxJsuspccxfsqUDvon9uts7UvkYZWjhhSCdPjJ6t5esrecX+UytFsKNE2lA+iMcZ2agBAJyRSYtIs1aR+5PHkQxP8URcBpHh7J89XtiA3/teKJrMULsbb9QaNg27U2PI8fQ90aLxPOpcuelOuH80G0M6BPZGA=~1; nguest=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnJhV1FpT2lJeVlUSmlaalZqTWpGbU5EZzBNVFV6WVRsbE0yWmxNelF4TjJGaFpURTJZU0lzSW1saGRDSTZNVFkxT0RVM05EQTVPSDAuZkhhcTNCY05adHdzdEJOYmVrM3Q5cjZmQm5ZdnctQ2N6TXNkdGZmU2JnRSIsImlhdCI6MTY2MDkyMjE2M30.OztXSHorDq7UjpvzvKsPuqRf1SjophEbmVacF5HcNQQ; _nsc=nsv1.public.eyJzdGlkIjoiNDlmZWM0NzgtNWQxMi00OGU0LTk2ZWUtODgzOGJiZmE5NmE0Iiwic2lkIjoiMmEyYmY1YzIxZjQ4NDE1M2E5ZTNmZTM0MTdhYWUxNmEiLCJpYXQiOjE2NjA5MjIxNjMsInZpZCI6IjM0MWY0MzhiLTdjZmMtNGE0Zi04N2FhLWU5ZDBkZGQxZDM2NCIsImhvbWVwYWdlIjp7fX02emdrY0NqUTFmQXdqWElNYXFVMEhMRys0dm1NYUNhZVJDcEsxREMzTHRzPQ.MQ; ak_bmsc=D2BABE42B90EC55CC1E9300A794242C8~000000000000000000000000000000~YAAQPzorF61/AoyCAQAADhOvthDmHRWSOEp0Bf0K+JWTNF18RV5DhnXzPSHyxwe1N/0LwucBcvmhw0AnPNrHtkDtMnj/0SBLCM/X3u3jzDfHUvQjQTgmXJz4p/9re58ueHplsy4gLxW2JwiWG4vuoSFkHFbu0dcPxOEuAf/iO+uthptbPynVgKzmwrw33H+Mm5VfHSVTRh819xe0+rNX6A23XxQ2h9UOtnE0yhHmh5TwCp+pFxDX7KaOoLVcBLYDAKhuXirceSVplr3M4u3CzOmWUCgsTmp6Nrhlq9tcuS0Uw9MAvfZDmvhh+zJVcmBtWnj+jWipmWXn2V5B9nNYzos4KHKhCZrZpmkWfS50dNp307x4HAe/INjChsptKiUdfydOEw72YM9D/gvuihFWhd8HYOsLF4u75hlQdN31B+16LUHy0c+BNVssCKX1Wnzs4Z+Z; bm_sv=F0717CB0273A61815258B7EC77A13C20~YAAQPzorF81iA4yCAQAANj/AthC1TA9vD1JBTYAUqokvPQtxPgVFrVCQ9NbLbu5sPNjYqOrNIIMy+KUaAJfwX/Qymk/FAj2XypqJBt+li7O2vZNaF5l4Yaf60l7oqcUBdIICBBSD6onDcdEF8qEfEC3qf7Nb3OyomEHrnCnlFuzdxdOhbSnE61gXgW/vC8TYltY2/Vq7fYBgdTjXwC2eUp/j8Fm0Uj95Io1BgTrOjZea8XHWNHw11fVcq/DRog==~1; RT="z=1&dm=noon.com&si=b8437eea-94ad-4e36-8cac-b182d2efe0a9&ss=l70m62kl&sl=2&tt=1dtw&rl=1&ul=r76n&hd=r8d3"; _etc=OpXYfOnXi1iVcEnm',
            'if-none-match': 'W/"1b130-EorCNMmXTPeEDgd96097zozg5j8"',
            'referer': 'https://www.noon.com/uae-en/fashion/fashion-men/?limit=50&page=4',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-cms': 'v3',
            'x-content': 'desktop',
            'x-locale': 'en-ae',
            'x-mp': 'noon',
            'x-platform': 'web',
        }

        params = {
            'limit': '50',
            'page': f'{i}',
        }
        print(f'Processing page {i}/{page}')
        free_proxy = FreeProxy(country_id='US', timeout=1000).get()
        print(f'1st {free_proxy}')
        response = requests.get(f'https://www.noon.com/_svc/catalog/api/v3/u{product_url[27:]}', timeout=160,
                                params=params, cookies=cookies, headers=headers, proxies=free_proxy).json()

        product_names = response.get('hits')
        try:
            for name in product_names:
                if name['sale_price']:
                    if int(name['sale_price']) / int(name['price']) < 0.25 and name['is_buyable']:
                        print(
                            f'{name["brand"]} {name["name"]} https://www.noon.com/uae-en/{name["url"]}/{name["sku"]}/p/?o={name["offer_code"]}')
                        fashion_list.append(
                            {
                                'title': name["brand"] + ' ' + name["name"],
                                'link': f'https://www.noon.com/uae-en/{name["url"]}/{name["sku"]}/p/?o={name["offer_code"]}',
                                'old_price': f'{name["price"]} AED',
                                'new_price': f'{name["sale_price"]} AED',
                                'discount': str(
                                    round((1 - int(name['sale_price']) / int(name['price'])) * 100)) + '% Off'
                            }

                        )
                        number_of_goods = number_of_goods + 1
            print(f'So far found {number_of_goods} products')
        except:
            print('Fuck we lost it')
    with open(f'{product_url.replace("/", "-")[28:-1]}.json', 'w', encoding='utf-8') as file:
        json.dump(fashion_list, file, indent=4, ensure_ascii=False)


def get_goods_to_json(URL):
    free_proxy = FreeProxy(country_id='US', timeout=1000).get()
    print(free_proxy)
    req = requests.get(URL, proxies=free_proxy)
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

    return page_number
    for page in range(1, page_number):

        time.sleep(0.1)
        # browser = webdriver.Chrome()
        # browser.get(f'{URL}?limit=50&page={page}')
        #
        # html = browser.page_source
        # req = requests.get(f'{URL}?limit=50&page={page}', HEADERS)

        src = req.text
        print(URL + f'?limit=50&page={page}')
        soup = BeautifulSoup(src, 'html')
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

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    for URL in URLS:
        collect_data(get_goods_to_json(URL), URL)

    # for URL in URLS:
    #     get_goods_to_json(URL)
    #
    # with open('log.txt', 'w') as file:
    #     file.write('done')
    # file.close()


if __name__ == '__main__':
    main()
