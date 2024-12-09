import asyncio
import aiohttp


async def main():

    session = aiohttp.ClientSession()

    # response = await session.post(
    #     "http://127.0.0.1:8080/user",
    #     json={
    #         "name": "Tony",
    #         "email": "stark@yandex.ru",
    #         "password": "user1 password"
    #     }
    # )
    # print(response.status)
    # print(await response.json())


    response = await session.get(
        "http://127.0.0.1:8080/user/1",
    )
    print(response.status)
    print(await response.text())

asyncio.run(main())