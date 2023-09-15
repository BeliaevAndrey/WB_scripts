"""
Получить список новых сборочных заданий
https://openapi.wildberries.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1new/get
Возвращает список всех новых сборочных заданий у продавца на данный момент.


Response Schema: application/json
200
orders -- Array of objects (Order) -- Список новых сборочных заданий
401 -- ошибка авторизации
403 -- доступ запрещен
429 -- превышен лимит по запросам
500 -- ошибка сервера
"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/orders/new"


async def market_get_orders_new():

    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()

if __name__ == '__main__':
    import pprint

    pprint.pp(asyncio.run(market_get_orders_new()))
