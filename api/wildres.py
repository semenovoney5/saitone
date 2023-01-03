import aiohttp
from lxml import etree
import asyncio
import re
from itertools import zip_longest
from models import myconn
from datetime import datetime


res = 1

class Wildres:
    def __init__(self):
        pass
        #
        #asyncio.run(self.main())

    
    async def fetch(self, session,url):
        
        proxy = "http://173.212.229.53:3128"
        async with session.get(url,proxy=proxy) as response:
            await asyncio.sleep(30)
            # 1. Extracting the Text:
            text = await response.text()
            # 2. Extracting the  Tag:
            title_tag = await self.parse_pages(text)
            print(title_tag)
    
    

    



    async def parse_pages(self,doc):
        response = etree.HTML(doc)
        conne = await  myconn()
        #curs = conn.cursor()
        #cur = conn.cursor()
        paterrn = r'(magnet:\?xt=urn:btih):([a-zA-Z0-9]+)'
        global res
        item = {}
        url = "test"
        
        size = response.xpath('//tr[@class="gai"]//td[3]/text()')
        print(url)
        razdayt = response.xpath('//td[@align="center"]//span[1]/text()')
        kachayt = response.xpath('//td[@align="center"]//span[2]/text()')
        gai = response.xpath('//*[@class="gai"]//a/text()')
        tum = response.xpath('//*[@class="tum"]//a/text()')
        magai = response.xpath('//*[@class="gai"]//a[2]/@href')
        matum = response.xpath('//*[@class="tum"]//a[2]/@href')
        title = [y for x in zip_longest(gai, tum) for y in x if y is not None]
        magnet = [y for x in zip_longest(magai, matum) for y in x if y is not None]
        
        created = datetime.now().strftime("%d-%m-%Y")
        print(magnet,"MMMMMMMMMMMMMM")
        for zsize,ztitle,zmagnet,zrazdayt,zkachayt in zip(size,title,magnet,razdayt,kachayt):
            print("zzzzzzzzzzz",zmagnet)
            item = {
                'url': url,
                'magnet': zmagnet,
                'title': ztitle,
                #'image': response.xpath('//*[@id="details"]//img/@src').extract_first(),
                #'descrypt': response.xpath('//*[@id="details"]/tbody/tr[1]/td[2]/text()[8]').extract_first(),
                'created':datetime.now().strftime("%d-%m-%Y"),
                'razdayt': zrazdayt,
                'kachayt': zkachayt,
                'info_hash': re.search(paterrn,zmagnet).group(2),
                'size':zsize


            }



            ####################created#####################
            await conne.execute('''INSERT INTO rutor(title,url,seeds,peers,magnet,created,updated,info_hash,size) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9)''',item['title'],item['url'],item['razdayt'],item['kachayt'],item['magnet'],item['created'],item['created'],item['info_hash'],item['size'])

            #await conne.close()

            ####################updated#####################

            #conn.execute('''UPDATE  rutor SET title=%s,url=%s,seeds=%s,peers=%s,magnet=%s,updated=%s,info_hash=%s,size=%s WHERE id = %s''',(item['title'],item['url'],item['razdayt'],item['kachayt'],item['magnet'],created,item['info_hash'],item['size'],res))
            #conn.commit()
            ####################################################
            res+=1
            print(res)
           
