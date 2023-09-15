"""
Создать склад продавца
https://openapi.wildberries.ru/#tag/Marketplace-Sklady/paths/~1api~1v3~1warehouses/post
Создает склад продавца. Нельзя привязывать склад WB, который уже используется.


Request Body schema: application/json
name(REQUIRED)-- string [ 1 .. 200 ] characters -- Имя склада продавца
officeId (REQUIRED) -- integer -- ID склада WB


201 -- список складов
Response Schema: application/json
id -- integer <int64> -- ID склада продавца

Response sample
{
  "id": 2
}

401 -- ошибка авторизации
403 -- доступ запрещен
404 -- ресурс не найден
429 -- превышен лимит запросов
500 -- ошибка сервера
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/warehouses"


async def market_post_create_seller_warehouse(name, officeId):

    headers_dict = {
        "Authorization": __token
    }

    payload = {
        "name": name,
        "officeId": officeId
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=payload) as response:
            if response.status == 201:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
            "name": "Склад Коледино",
            "officeId": 15
    }

    pprint.pp(asyncio.run(market_post_create_seller_warehouse(**sample_data)))
