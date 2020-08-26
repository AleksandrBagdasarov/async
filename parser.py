import asyncio
import timeit
from urllib.parse import urljoin

import aiohttp
from parsel import Selector

start_t = timeit.default_timer()

DOMAIN = 'https://www.octoparse.com/'

URLS = ('https://www.octoparse.com/blog',)


async def main():   
    async with aiohttp.ClientSession() as session:
        task = [get_pages(session, url) for url in URLS]
        await asyncio.wait(task)


async def get_pages(session, url):
    print(url)
    async with session.get(url) as response:
        selector = Selector(text=await response.text())
        task = []
        for link in [selector.xpath("//a[@class='full pc_show']/@href").extract_first()]:
            print(link)
            task.append(extract_card(session, urljoin(DOMAIN, link)))

        await asyncio.wait(task)
        
        if task:
            print(task)



async def extract_card(session, url):
    # await asyncio.sleep(4)
    async with session.get(url) as response:
        selector = Selector(text=await response.text())
        text = text_cleaner(selector.xpath("//div[@class='article']/div[@class='content']//text()").extract())
        with open('text.txt', 'a') as f:
            f.write(text)


def text_cleaner(full_text: list) -> str:
    clean_text = [clean(text) for text in full_text if clean(text)]
    return clean('\n***\n'.join(clean_text))

def clean(text: str) -> str:
    return text.replace('***', '').replace('  ', '').replace('\t', '').replace('\n', '')

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




# asyncio.run(start(extract_links, URLS))








if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


stop = timeit.default_timer()
# print(len(d['data']), d['data'])
print('Time: ', stop - start_t) 
