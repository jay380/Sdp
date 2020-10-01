import socketio
from selectorlib import Extractor
import requests
from time import sleep
from flask import Flask, render_template, request
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
import asyncio

headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'}
headers2 = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.flipkart.com',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
# Create an Extractor by reading from the YAML file
# loop = asyncio.get_event_loop()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index1.html")


image_data = []


async def add_images_urls(data, url):
    i = 0
    # session = HTMLSession()
    # response = session.get(url)
    # response.html.render(sleep=1, scrolldown=20)
    asession = AsyncHTMLSession()
    r = await asession.get(url)
    await r.html.arender(sleep=1, scrolldown=20)
    response = r.html.raw_html
    div = response.html.find('._1UoZlX')
    for image in div:
        img = image.find('img', first=True)
        img_src = img.attrs['src']
        image_data.append(img_src)

    for product in data.values():
        for item in product:
            item['url'] = 'https://www.flipkart.com' + item['url']
            if i < len(image_data):
                item['image'] = image_data[i]
                i += 1
    return data


@app.route('/', methods=['POST'])
def scrape():
    e1 = Extractor.from_yaml_file('search_result.yml')
    e2 = Extractor.from_yaml_file('flip_results.yml')
    text = request.form.get("search_bar")
    print(text)
    url1 = "https://www.amazon.in/s?k={0}&rh=n%3A1375424031&ref=nb_sb_noss".format(text)
    url2 = "https://www.flipkart.com/search?q={0}&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_HistoryAutoSuggest_1_7_na_na_na&otracker1=AS_QueryStore_HistoryAutoSuggest_1_7_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=macbook+pro%7CLaptops&requestId=4b1460e8-fcf5-4369-a655-a2501be025a8&as-backfill=on".format(text)
    r1 = requests.get(url1, headers=headers1)
    r2 = requests.get(url2, headers=headers2)
    sleep(2)
    data1 = e1.extract(r1.text)
    data2 = e2.extract(r2.text)
    product_title1 = []
    product_price1 = []
    product_img1 = []
    product_url1 = []
    product_title2 = []
    product_price2 = []
    product_img2 = []
    product_url2 = []
    i = 0

    for product1 in data1.values():
        for item1 in product1:
            product_title1.append(item1['title'])
            product_price1.append(item1['price'])
            product_img1.append(item1['image'])
            new_url1 = 'https://www.amazon.in' + item1['url']
            product_url1.append(new_url1)

    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    data3 = asyncio.get_event_loop().run_until_complete(add_images_urls(data2, url2))
    # data3 = asyncio.run(add_images_urls(data2, url2))
    # data3 = await add_images_urls(data2, url2)
    # data3 = loop.run_until_complete(add_images_urls(data2, url2))
    # data3 = add_images_urls(data2, url2)
    for product2 in data3.values():
        for item2 in product2:
            product_title2.append(item2['title'])
            product_price2.append(item2['price'])
            product_img2.append(item2['image'])
            product_url2.append(item2['url'])
            # new_url2 = 'https://www.flipkart.com' + item2['url']
            # product_url2.append(new_url2)


    # session = HTMLSession()
    # response = session.get(url2)
    # response.html.render(sleep=1, scrolldown=20)
    # # Container for each product being displayed
    # div = response.html.find('._1UoZlX')
    # for image in div:
    #     img = image.find('img', first=True)
    #     img_src = img.attrs['src']
    #     product_img2.append(img_src)

    return render_template("index2.html", title1=product_title1, price1=product_price1, img1=product_img1,
                           url1=product_url1, title2=product_title2, price2=product_price2, img2=product_img2, url2=product_url2)


if __name__ == "__main__":
    # socketio.run(app)
    app.run(debug=False)


