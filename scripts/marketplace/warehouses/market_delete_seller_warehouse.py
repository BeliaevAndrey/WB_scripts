"""
Удалить склад продавца
https://openapi.wildberries.ru/#tag/Marketplace-Sklady/paths/~1api~1v3~1warehouses~1{warehouseId}/delete
Создает склад продавца. Нельзя привязывать склад WB, который уже используется.

path Parameters
warehouseId (REQUIRED) -- integer <int64> -- ID склада продавца

204 -- удалено
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


async def market_delete_seller_warehouse(warehouseId: int):
    headers_dict = {
        "Authorization": __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.delete(url=URL.format(warehouseId=warehouseId)) as response:
            if response.status == 201:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "warehouseId": 809808,
    }

    pprint.pp(asyncio.run(market_delete_seller_warehouse(**sample_data)))
