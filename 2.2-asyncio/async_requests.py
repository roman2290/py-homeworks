#! C:\Users\User\Desktop\py-homeworks\2.2-asyncio\venv\Scripts\python.exe


import more_itertools
import asyncio
import aiohttp
import datetime
from models import Session, Person, init_orm, close_orm
from aiohttp import ClientSession


MAX_COROS = 10

async def get_url(url, key, session):
    async with session.get(f'{url}') as response:
        data = await response.json()
        return data[key]

async def get_urls(urls, key, session):
    tasks = (asyncio.create_task(get_url(url, key, session)) for url in urls)
    for task in tasks:
        yield await task

async def get_data(urls, key, session):
    result_list = []
    async for item in get_urls(urls, key, session):
        result_list.append(item)
    return ', '.join(result_list)

async def insert_people(json_list: list[dict]):
    async with Session() as session:
        async with ClientSession() as session_deep:
            for person_json in json_list:
                homeworld_str = await get_data([person_json['homeworld']], 'name', session_deep)
                films_str = await get_data(person_json['films'], 'title', session_deep)
                species_str = await get_data(person_json['species'], 'name', session_deep)
                starships_str = await get_data(person_json['starships'], 'name', session_deep)
                vehicles_str = await get_data(person_json['vehicles'], 'name', session_deep)
                swapi_people_list = [Person(
                        birth_year=item['birth_year'],
                        eye_color=item['eye_color'],
                        gender=item['gender'],
                        hair_color=item['hair_color'],
                        height=item['height'],
                        mass=item['mass'],
                        name=item['name'],
                        skin_color=item['skin_color'],
                        homeworld=homeworld_str,
                        films=films_str,
                        species= species_str,
                        starships=starships_str,
                        vehicle=vehicles_str) for item in json_list]
        session.add_all(swapi_people_list)
        await session.commit()


async def get_person(person_id, http_session):
    url = f'https://swapi.dev/api/people/{person_id}/'
    http_response = await http_session.get(url)
    json_data = await http_response.json()
    return json_data

async def main():
    await init_orm()


    async with aiohttp.ClientSession() as session:
        for i_list in more_itertools.chunked(range(1, 50), MAX_COROS):
            coros = [get_person(i, http_session=session) for i in i_list]
            result = await asyncio.gather(*coros)
            coro = await insert_people(result)
            asyncio.create_task(coro)

        tasks = asyncio.all_tasks()
        task_main = asyncio.current_task()
        tasks.remove(task_main)
        await asyncio.gather(*tasks)

    await close_orm()

start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)










