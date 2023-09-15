"""
Удалить метаданные сборочного задания
https://openapi.wildberries.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1{orderId}~1meta/delete

Возвращает метаданные заказа. Возможные метаданные imei, uin, gtin.

Path Parameters
orderId(REQUIRED) -- integer <int64> -- ID сборочного задания


Response Samples:
204 -- Удалено
400 -- некорректные данные
401 -- ошибка авторизации
403 -- доступ запрещен
409 -- ошибка удаления метаданных
429 -- превышен лимит по запросам
500 -- ошибка сервера
"""
from __future__ import annotations

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/orders/{orderId}/meta"


async def market_delete_orders_metadata(orderId):

    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.delete(url=URL.format(orderId=orderId)) as response:
            if response.status == 204:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = 5632423

    pprint.pp(asyncio.run(market_delete_orders_metadata(sample_data)))
