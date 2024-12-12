#! C:\Users\User\Desktop\py-homeworks\2.2-asyncio\venv\Scripts\python.exe

import asyncio
import datetime
import itertools
from aiohttp import ClientSession
import aiohttp
from more_itertools import chunked
from models import Session, engine
from models import Person, Base, init_orm, close_orm
import more_itertools


URL = 'https://swapi.dev/api/people/'
CHUNK_SIZE = 10

async def chunked_async(async_iter, size):
    buffer = []
    while True:
        try:
            item = async_iter.__anext__()
        except StopAsyncIteration:
            yield buffer
            break
        buffer.append(item)
        if len(buffer) == size:
            yield buffer
            buffer = []

async def get_person(person_id: int, session: ClientSession):
    async with session.get(f'{URL}/{person_id}') as response:
        json_person = await response.json()
        json_person['person_id'] = person_id
        return json_person

async def get_people():
    async with ClientSession as session:
        async with session.get(URL) as res:
            response = await res.json()
            page = int(response['count']) // 10 + 1
            page_res = await session.get(f'{URL}?page={page}')
            page_res = await page_res.json()
            count = int(page_res['results'][-1]['url'].split(sep='/')[-2]) + 1
        for chunk in chunked(range(1, count), CHUNK_SIZE):
            coroutines = [get_person(people_id=i, session=session) for i in chunk]
            results = await asyncio.gather(*coroutines)
            for item in results:
                yield item

async def extract_names(list_href: str | list, type_objects: str) -> str:
    list_names = []
    if isinstance(list_href, str):
        list_href = [list_href]
    for href in list_href:
        async with ClientSession() as session:
            response = await session.get(href)
            response = await response.json()
            list_names.append(response[type_objects])
    return ', '.join(list_names)


async def insert_person(people_chunk):
    person_list = [
        Person(
            birth_year=item['birth_year'],
            eye_color=item['eye_color'],
            films=await extract_names(item['films'], 'title'),
            gender=item['gender'],
            hair_color=item['hair_color'],
            height=item['height'],
            homeworld=await extract_names(item['homeworld'], 'name'),
            mass=item['mass'],
            name=item['name'],
            skin_color=item['skin_color'],
            species=await extract_names(item['species'], 'name'),
            starships=await extract_names(item['starships'], 'name'),
            vehicles=await extract_names(item['vehicles'], 'name')
        )
        for item in people_chunk if item.get('birth_year')]

    async with Session() as session:
        session.add_all(person_list)
        await session.commit()


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as http_session:
        for i_list in more_itertools.chunked(range(1, 101), CHUNK_SIZE):
            coros = [get_person(i, http_session) for i in i_list]
            result = await asyncio.gather(*coros)
            coro = insert_person(result)
            asyncio.create_task(coro)

        tasks = asyncio.all_tasks()
        task_main = asyncio.current_task()
        tasks.remove(task_main)
        await asyncio.gather(*tasks)
  
    await close_orm()

if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main(), debug=True)
    print(datetime.datetime.now() - start)



