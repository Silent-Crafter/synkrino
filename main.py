import requests
# import readline
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

headers = {
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "document",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}


def cache(filename: str, content: str):
    with open(filename, 'w') as f:
        f.write(content)


def amazon_scraper(resp: str):
    soup = BeautifulSoup(resp, 'lxml')

    titles = []
    prices = []
    links = []

    cards = soup.find_all('div', {'class': 's-card-container'})
    # print(cards[0])

    for card in cards:
        try:
            titles.append(card.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text)
            prices.append(card.find('span', {'class': 'a-price-whole'}).text)
            links.append("https://www.amazon.in" + card.a['href'])
        except AttributeError:
            pass

    symbol = soup.find('span', {'class': 'a-price-symbol'}).text
    prices = list(map(lambda x: symbol+x, prices))

    return titles, prices, links


def flipkart_scraper(resp: str):
    found_none = False
    soup = BeautifulSoup(resp, 'lxml')

    titles = []
    prices = []
    links = []

    cols = soup.find_all('div', {'class': '_13oc-S'})
    for col in cols:
        cards = list(col.children)
        if found_none:
            title = col.find('div', {'class': 'col-7-12'}).div.text
            price = col.find('div', {'class': 'col-5-12'}).div.div.div.text
            link = "https://www.flipkart.com" + col.a['href']

            titles.append(title)
            prices.append(price)
            links.append(link)

        else:
            for card in cards:
                title, price, link = None, None, None
                al = card.div.find_all('a')
                for a in al:
                    try:
                        title = a['title']
                        link = "https://www.flipkart.com" + a['href']
                    except KeyError:
                        pass

                    try:
                        t = a.div.div.text
                        if t:
                            price = t
                    except AttributeError:
                        pass

                # print(title, price, link)
                if title == None or price == None:
                    found_none = True
                    break

                titles.append(title)
                prices.append(price)
                links.append(link)

    return titles, prices, links


query = input("Enter a query: ")
amazon_url = "https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" + quote_plus(query)
flipkart_url = "https://www.flipkart.com/search?q=" + quote_plus(query) + "&marketplace=FLIPKART&otracker=start&as-show=on&as=off"

amz_resp = requests.get(amazon_url, headers=headers)
flp_resp = requests.get(flipkart_url, headers=headers)

amz_file = 'amazon.html'
flp_file = 'flipkart.html'

#cache(amz_file, amz_resp.text)
#cache(flp_file, flp_resp.text)

#with open(amz_file, 'r') as f:
#    amz_resp_html = f.read()

#with open(flp_file, 'r') as f:
#    flp_resp_html = f.read()


#amz_titles, amz_prices = amazon_scraper(amz_resp_html)
#flp_titles, flp_prices, links = flipkart_scraper(flp_resp_html)

amz_titles, amz_prices, amz_links = amazon_scraper(amz_resp.text)
flp_titles, flp_prices, flp_links = flipkart_scraper(flp_resp.text)

print(len(amz_titles), len(amz_prices))
print(len(flp_titles), len(flp_prices))

print("\nAmazon search results: ")
print('-' * 100)
for title, price, link in zip(amz_titles, amz_prices, amz_links):
    print()
    print('-' * 100)
    print(title, ':-\nPrice', price, '\nLink:', link)
    print('-'*100)
    print()

print("\nFlipkart search results: ")
print('-' * 100)
for title, price, link in zip(flp_titles, flp_prices, flp_links):
    print()
    print('-' * 100)
    print(title, ':-\nPrice: ', price, '\nLink: ', link)
    print('-' * 100)
    print()
