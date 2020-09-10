import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'}


def amazon():
    url = 'https://www.amazon.in/s?k=asus&rh=n%3A1375424031&ref=nb_sb_noss'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.select('.a-color-base.a-text-normal')
    prices = soup.find_all(class_='a-price-whole')
    print(titles)
    for title in titles:
        print(title.get_text())
    for price in prices:
        print(price.text)

    print(titles[1])
    print(prices[1])


amazon()