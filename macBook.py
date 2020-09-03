import requests
from bs4 import BeautifulSoup

# section = soup.find('div', class_="a-section a-spacing-medium")
# for section in soup.find_all('div', class_="a-section a-spacing-medium"):
#    # print(first.prettify()
#   info = section.find('div', class_="sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 "
#                                      "sg-col sg-col-28-of-36 sg-col-20-of-28")
#    # print(info.prettify())
#   title = info.find('span', class_="a-size-medium a-color-base a-text-normal")
#    print('\n')
#   print(title.text)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/58.0.3029.110 Safari/537.3'}


def amazon():
    url = 'https://www.amazon.in/Apple-MacBook-16-inch-Storage-Intel-Core-i7/dp/B081JWZQJB/ref=sr_1_2?'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    print("Amazon deal: ")
    print(title.strip())
    print(price)


def flipkart():
    url = 'https://www.flipkart.com/apple-macbook-pro-core-i7-9th-gen-16-gb-512-gb-ssd-mac-os-catalina-4-graphics' \
          '-mvvj2hn-a/p/itm0a25cefe31533? '
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find(class_="_35KyD6").get_text()
    price = soup.find(class_="_1vC4OE _3qQ9m1").get_text()
    print("Flipkart deal: ")
    print(title.strip())
    print(price)


def website():
    url = 'https://www.apple.com/in/macbook-pro-16/specs/'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
#    title = soup.find(class_="_35KyD6").get_text()
#    price = soup.find_all('div', class_="column  large-6"
    main = soup.find_all(class_="column large-6")[2]
#    prices = main.find_all(class_="")
#    row = main.index("class=row")
    print("Website deal: ")
    print('MacBook Pro', main.text)


amazon()
flipkart()
website()
