from selectorlib import Extractor
import requests
from time import sleep


e = Extractor.from_yaml_file('search_results.yml')

# url = 'https://www.amazon.in/s?k=lenovo&i=computers&rh=n%3A1375424031%2Cp_89%3ALenovo&dc&qid=1599827986&rnid=3837712031&ref=sr_nr_p_89_1'
url = 'https://www.amazon.in/s?k=dell&rh=n%3A1375424031&ref=nb_sb_noss'
text = 'lenovo'
ram = '8GB'
storage = '1TB'


def scrape(url):

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.in/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    print(f"Downloading {url}")
    r = requests.get(url, headers=headers)
    sleep(2)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    return e.extract(r.text)


filtered_products = []
product_data = []
url_data = []


def filters(data):
    if data:
        for product in data.values():
            for item in product:
                print(f"Saving Product: {item['title']}")
                if ram in ''.join(item['title'].split()) and storage in ''.join(item['title'].split()):
                    filtered_products.append(item)


def fix_url(data):
    if data:
        for product in data.values():
            for item in product:
                item['url'] = 'https://www.amazon.in' + item['url']
    return data


def main():
    data = scrape(url)
    # filters(data)
    for product in data.values():
        for item in product:
            product_data.append(item)
    first_five_products = product_data[:5]
    # print(first_five_products)

    new_data = fix_url(data)
    print(new_data)


    # for value in first_five_products:
    #     print(value['title'])
    #     print(value['price'])


main()

