import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'}
#########################
#
# def amazon(url):
#     # url = 'https://www.amazon.in/Apple-MacBook-16-inch-Storage-Intel-Core-i7/dp/B081JWZQJB/ref=sr_1_2?'
#     res = requests.get(url, headers=headers)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     print("Amazon deal: ")
#     try:
#         title = soup.find(id="productTitle").get_text()
#         price = soup.find(id="priceblock_ourprice").get_text()
#     except AttributeError:
#         print("Currently unavailable")
#     else:
#         print(title.strip())
#         print(price)
#
#
# def flipkart(url):
#     # url = 'https://www.flipkart.com/apple-macbook-pro-core-i7-9th-gen-16-gb-512-gb-ssd-mac-os-catalina-4-graphics' \
#     #       '-mvvj2hn-a/p/itm0a25cefe31533? '
#     res = requests.get(url, headers=headers)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     print("Flipkart deal: ")
#     try:
#         title = soup.find(class_="_35KyD6").get_text()
#         price = soup.find(class_="_1vC4OE _3qQ9m1").get_text()
#     except AttributeError:
#         print("Currently unavailable")
#     else:
#         print(title.strip())
#         print(price)
#
#
# text = 'MacBook pro'
# size = '13'
# text1 = 'AlienWare M15'
# device_dict = {
#     'macbookpro_ama': {
#         # size
#         '16': {
#             # ram
#             '16': {
#                 '1tb': 'Currently unavailable',
#                 '512gb': 'https://www.amazon.in/Apple-MacBook-16-inch-Storage-Intel-Core-i7/dp/B081JWZQJB/ref=sr_1_2?',
#                 '256gb': 'Currently unavailable',
#             },
#             '8': {
#
#             }
#         },
#         '13': 'https://www.amazon.in/Apple-MacBook-Pro-10th-Generation-Intel-Core-i5/dp/B0883K1BX4/ref=sr_1_4?'
#     },
#
#     'macbookpro_flip': {
#         '16': 'https://www.flipkart.com/apple-macbook-pro-core-i7-9th-gen-16-gb-512-gb-ssd-mac-os-catalina-4-graphics-mvvj2hn-a/p/itm0a25cefe31533?',
#         '13': 'https://www.flipkart.com/apple-macbook-pro-core-i5-8th-gen-8-gb-512-gb-ssd-mac-os-mojave-mv972hn/p/itmfgnhg4gddustb?'
#
#     },
#     'alienwarem15_ama': 'https://www.amazon.in/Dell-Alienware-M15-R2-15-6-inch/dp/B07XZHXKDN/ref=sr_1_2?',
#     'alienwarem15_flip': 'https://www.flipkart.com/alienware-core-i7-10th-gen-16-gb-512-gb-ssd-windows-10-home-6-graphics-nvidia-geforce-gtx-1660-ti-m15r3-gaming-laptop/p/itme9ee3d237303f?'
# }
#
# url_list = []
# for k, v in device_dict.items():
#     if ''.join(text.lower().strip().split()) in k:
#         # url_list.append(v)
#         for k1, v1 in v.items():
#             if k1 == size:
#                 url_list.append(v1)
#
# url_ama = url_list[0]
# url_flip = url_list[1]
#
#
# def scrapes(url1, url2):
#     amazon(url1)
#     flipkart(url2)
#
#
# scrapes(url_ama, url_flip)
###############################
text = 'MacBook Pro'
size = '16'
ram = '16GB'
storage = '1TB'


def get_text(item):
    return item.text


def amazon(url):
    # url = 'https://www.amazon.in/s?k=macbook+pro&rh=n%3A1375424031%2Cp_89%3AApple&dc&'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all(class_='a-size-medium a-color-base a-text-normal')
    prices = soup.find_all(class_='a-offscreen')
    titles_text = list(map(get_text, titles))
    prices_text = list(map(get_text, prices))
    device_list = list(zip(titles_text, prices_text))

    def filters(item):
        title_list = item[0].split()
        spec_list = title_list[:]
        spec_str = ''.join(spec_list)
        if ''.join(text.lower().strip().split()) in spec_str.lower():
            if size.lower() in spec_str.lower() and ram.lower() in spec_str.lower():
                return item

    filtered_device_list = list(filter(filters, device_list))
    return filtered_device_list


def flipkart(url):
    # url = 'https://www.flipkart.com/search?q=macbook+pro&'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all(class_='_3wU53n')
    prices = soup.find_all(class_='_1vC4OE _2rQ-NK')
    titles_text = list(map(get_text, titles))
    prices_text = list(map(get_text, prices))
    device_list = list(zip(titles_text, prices_text))

    def filters(item):
        title_list = item[0].split()
        spec_list = title_list[:]
        spec_str = ''.join(spec_list)
        if ''.join(text.lower().strip().split()) in spec_str.lower():
            if storage.lower() in spec_str.lower() and ram.lower() in spec_str.lower():
                return item

    filtered_device_list = list(filter(filters, device_list))
    return filtered_device_list


device_dict = {
    'macbookpro_ama': 'https://www.amazon.in/s?k=macbook+pro&rh=n%3A1375424031%2Cp_89%3AApple&dc&',
    'macbookpro_flip': 'https://www.flipkart.com/search?q=macbook+pro&',
    'alienware_ama': 'https://www.amazon.in/s?k=alienware+laptop&rh=n%3A1375424031%2Cp_89%3ADell&dc&crid=210UIGFUO2G7T&',
    'alienware_flipkart': 'https://www.flipkart.com/search?q=alienware+laptops&sid=6bo%2Cb5g&as=on&as-show=on&'
}


def scrapes():
    url_list = []
    for k, v in device_dict.items():
        if ''.join(text.lower().strip().split()) in k:
            if v not in url_list:
                url_list.append(v)

    url_ama = url_list[0]
    url_flip = url_list[1]
    ama_list = amazon(url_ama)
    flip_list = flipkart(url_flip)
    print('Amazon deal: ')
    for item, value in ama_list:
        print(f"\tTitle: {item}")
        print(f"\tPrice: {value}")

    print('Flipkart deal: ')
    for item, value in flip_list:
        print(f"\tTitle: {item}")
        print(f"\tPrice: {value}")


scrapes()