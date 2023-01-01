import aiohttp
import asyncio
from lxml import etree
from wildres import Wildres




# listUrl=['http://rutor.info/search/{page}/0/000/0/%D0%9A%D0%9F%D0%9A']

async def main():
    Mywilds = Wildres()
    
    tasks = []
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        for url in range(1,19):
            tasks.append(Mywilds.fetch(session,f'http://rutor.info/search/{url}/0/000/0/%D0%9A%D0%9F%D0%9A'))
            print("count",url,f'http://rutor.info/search/{url}/0/000/0/%D0%9A%D0%9F%D0%9A')

        htmls = await asyncio.gather(*tasks)
    
asyncio.run(main())