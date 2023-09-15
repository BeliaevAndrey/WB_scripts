"""
Обновить склад
https://openapi.wildberries.ru/#tag/Marketplace-Sklady/paths/~1api~1v3~1warehouses~1{warehouseId}/put
Обновляет склад продавца. Изменение выбранного склада WB допустимо раз в сутки.
Нельзя привязывать склад WB, который уже используется.


path Parameters
warehouseId (REQUIRED) -- integer <int64> -- ID склада продавца

Request Body schema: application/json
name (REQUIRED)-- string [ 1 .. 200 ] characters -- Имя склада продавца
officeId (REQUIRED) -- integer-- Идентификатор склада WB

204 -- Обновлено
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

URL = "https://suppliers-api.wildberries.ru/api/v3/warehouses/{warehouseId}"


async def market_put_renew_seller_warehouse(warehouseId: int, name: str, officeId: int):
    headers_dict = {
        "Authorization": __token
    }

    payload = {
        "name": name,
        "officeId": officeId
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.put(url=URL.format(warehouseId=warehouseId),
                                  json=payload) as response:
            if response.status == 204:
                return await response.text()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "warehouseId": 809808,
        "name": "Склад Коледино",
        "officeId": 15
    }

    pprint.pp(asyncio.run(market_put_renew_seller_warehouse(**sample_data)))
