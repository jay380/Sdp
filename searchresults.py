from selectorlib import Extractor
import requests
import json
from time import sleep


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('search_results.yml')


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

    # Download the page using requests
    print(f"Downloading {url}")
    r = requests.get(url, headers=headers)
    sleep(2)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)

# product_data = []

# url = 'https://www.amazon.in/s?k=lenovo&i=computers&rh=n%3A1375424031%2Cp_89%3ALenovo&dc&qid=1599827986&rnid=3837712031&ref=sr_nr_p_89_1'
url = 'https://www.amazon.in/s?k=dell&rh=n%3A1375424031&ref=nb_sb_noss'
text = 'lenovo'
ram = '8GB'
storage = '1TB'

# with open('search_results_output.jsonl', 'w') as outfile:
data = scrape(url)
filtered_products = []
# print(data)
if data:
    for product in data.values():
        # product['search_url'] = url
        for item in product:
            print(f"Saving Product: {item['title']}")
            if ram in ''.join(item['title'].split()) and storage in ''.join(item['title'].split()):
                filtered_products.append(item)
        # # json.dump(product, outfile)
        # # outfile.write("\n")


print(filtered_products)