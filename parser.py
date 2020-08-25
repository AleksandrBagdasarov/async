import asyncio
import timeit
from urllib.parse import urljoin

import aiohttp
from parsel import Selector

start_t = timeit.default_timer()

DATA = []
DOMAIN = 'https://auto.ria.com/newauto/'
START_URLS = ('https://auto.ria.com/newauto/search/?page=1&show_in_search=1&markaId=55&size=100',
              'https://auto.ria.com/newauto/search/?page=1&show_in_search=1&markaId=9&size=100',
              'https://auto.ria.com/newauto/search/?page=1&show_in_search=1&markaId=24&size=100')


async def main():
    async with aiohttp.ClientSession() as session:
        task = [get_pages(session, url) for url in START_URLS]
        await asyncio.wait(task)


async def get_pages(session, url):
    async with session.get(url) as response:
        selector = Selector(text=await response.text())
        task = [extract_card(session, urljoin(DOMAIN, link)) for link in selector.xpath("//h3/a/@href").extract()]
        await asyncio.wait(task)


async def extract_card(session, url):
    async with session.get(url) as response:
        selector = Selector(text=await response.text())
        price = selector.xpath("//section/div[@class='price_value']/text()").extract_first()
        name = selector.xpath("//h1/text()").extract_first()
        DATA.append((price, name))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

stop = timeit.default_timer()
with open('Autoria.csv', 'w') as f:
    for line in DATA:
        f.write(f'{line}\n')

print('Time: ', stop - start_t)
