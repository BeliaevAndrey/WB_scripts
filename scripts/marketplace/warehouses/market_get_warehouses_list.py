"""
Получить список складов WB
https://openapi.wildberries.ru/#tag/Marketplace-Sklady/paths/~1api~1v3~1offices/get
Возвращает список всех складов WB для привязки к складам продавца.

200 -- список складов
401 -- ошибка авторизации
403 -- доступ запрещен
429 -- превышен лимит запросов
500 -- ошибка сервера
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/offices"


async def market_get_warehouses_list():

    headers_dict = {
        "Authorization": __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    pprint.pp(asyncio.run(market_get_warehouses_list()))
