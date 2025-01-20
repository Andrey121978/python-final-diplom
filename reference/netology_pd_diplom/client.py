
import aiohttp
import asyncio

async def main():
    async with (aiohttp.ClientSession() as session):
        response1 = await session.post("http://127.0.0.1:8000/api/v1/user/register", json={
        'first_name': 'Andrew',
        'last_name': 'Kibirev',
        'email': 'kibirev@bk.ru',
        'password': '12345ASd',
        'company': 'Best',
        'position': 'director',
    })
        print(response1)
        response2 = await session.post("http://127.0.0.1:8000/api/v1/user/login", json={
        'email': 'kibirev@bk.ru',
        'password': '12345ASd',
        })
        print(response2)
        # response3 = await session.post("http://127.0.0.1:8080/ads", json={
        #     'title': 'Продам электропилу',
        #     'description': 'Продам торцовочную пилу',
        #     'owner': 'Алексей',
        # })
        #
        #
        response_get = await session.get("http://127.0.0.1:8000/api/v1/user/details")
        print(response_get)
        #
        #
        # response_delete = await session.delete("http://127.0.0.1:8080/ads/2")
        # print(response_delete)

# Запуск основной асинхронной функции
if __name__ == '__main__':
    asyncio.run(main())