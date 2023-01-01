import requests
import json
import asyncio
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError



api_key ='2dacd55e6ca326b523c0eadf77dc844b'





async def fetch(url, session):
    """Fetch a url, using specified ClientSession."""
    try:
         async with session.get(url) as response:
         # print(f"fetching {url}")
            resp = await response.read()
            return json.loads(resp)

    except asyncio.TimeoutError:
        return {"results": f"timeout error on {url}"}


async def get_movie(query):
    

    URLM =f'http://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}&page=1&language=ru'
    async with aiohttp.ClientSession() as session:
        try:


       
            task = asyncio.create_task(fetch(URLM,session))
    	        
    	        
            resp = await task
            elmd = {}
            print(resp)
            if resp['results'] == []:
                elmd['vote_average']=0
                elmd['original_title']="net dannix"
                elmd['overview']="net dannix"
                elmd['poster_path']="net dannix"
                return elmd['vote_average'],elmd['original_title'],elmd['overview'],elmd['poster_path']

            else:    
                for elm in resp['results']:

                    return elm['vote_average'],elm['original_title'],elm['overview'],elm['poster_path']
                    print(elm['overview'],elm['poster_path'])
                    print('https://image.tmdb.org/t/p/w500'+elm['poster_path'])   
        except ClientConnectorError as e:
            print(elmd)
            return elmd


if __name__ == '__main__':
    asyncio.run(get_movie("Фантастические грибы"))