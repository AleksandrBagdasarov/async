import asyncio
import timeit
from urllib.parse import urljoin

import aiohttp
from parsel import Selector

start_t = timeit.default_timer()

DOMAIN = 'https://auto.ria.com/'

URLS = ('https://auto.ria.com/newauto/marka-hyundai/',
         'https://auto.ria.com/newauto/marka-nissan/',
)




async def get_pages(session, url):
    async with session.get(url) as response:
        selector = Selector(text=await response.text())
        task = [extract_card(session, urljoin(DOMAIN, link)) for link in selector.xpath("//h3/a/@href").extract()]
        await asyncio.wait(task)
        
        # //div[@id='marks-block']/a[contains(.,'yundai')]
# URLS = ('11111', '33333', '55555')

# async def start(func, list_):
#     task = [func(x) for x in list_]    
#     await asyncio.wait(task)

#     # for x in range(1,6):
#     #     asyncio.ensure_future(say_after(1,x))

# async def extract_links(url):
#     # get_link
#     await asyncio.sleep(0.5)
#     print(url)
#     task = [extract_card(x) for x in (url)]
#     await asyncio.wait(task)


async def extract_card(session, url):
    await asyncio.sleep(4)
    async with session.get(url) as response:
        selector = Selector(text=await response.text())
        print(selector.xpath("//section/div[@class='price_value']/text()").extract_first())



# asyncio.run(start(extract_links, URLS))





async def main():   
    async with aiohttp.ClientSession() as session:
        task = [get_pages(session, url) for url in URLS]
        await asyncio.wait(task)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


stop = timeit.default_timer()
# print(len(d['data']), d['data'])
print('Time: ', stop - start_t) 
