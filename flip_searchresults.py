from selectorlib import Extractor
from requests_html import HTMLSession
import requests
from time import sleep

e = Extractor.from_yaml_file('flipkart1.yml')

# url = 'https://www.amazon.in/s?k=lenovo&i=computers&rh=n%3A1375424031%2Cp_89%3ALenovo&dc&qid=1599827986&rnid=3837712031&ref=sr_nr_p_89_1'
url = 'https://www.flipkart.com/search?q=macbook+pro&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_HistoryAutoSuggest_1_7_na_na_na&otracker1=AS_QueryStore_HistoryAutoSuggest_1_7_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=macbook+pro%7CLaptops&requestId=4b1460e8-fcf5-4369-a655-a2501be025a8&as-backfill=on'
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
        'referer': 'https://www.flipkart.com/',
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
image_data = []


def filters(data):
    if data:
        for product in data.values():
            for item in product:
                print(f"Saving Product: {item['title']}")
                if ram in ''.join(item['title'].split()) and storage in ''.join(item['title'].split()):
                    filtered_products.append(item)


def images():
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1, scrolldown=20)
    # Container for each product being displayed
    div = response.html.find('._1UoZlX')
    for image in div:
        img = image.find('img', first=True)
        img_src = img.attrs['src']
        image_data.append(img_src)


def main():
    data = scrape(url)
    # filters(data)
    for product in data.values():
        for item in product:
            product_data.append(item)
    first_five_products = product_data[:5]
    # print(first_five_products)
    print(data)
    images()
    for i in image_data:
        print(i)
    # for i in image_data:
    #     print(i)


main()

