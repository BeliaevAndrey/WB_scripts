"""
Получить метаданные сборочного задания
https://openapi.wildberries.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1{orderId}~1meta/get

Возвращает метаданные заказа. Возможные метаданные imei, uin, gtin.

Path Parameters
orderId(REQUIRED) -- integer <int64> -- ID сборочного задания


Response Samples:
200
{
  "meta": {
    "imei": 123456789012345,
    "uin": 1234567890123456
  }
}

401 -- ошибка авторизации
403 -- доступ запрещен
404 -- запрашиваемый ресурс не найден
500 -- ошибка сервера
"""
from __future__ import annotations

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/orders/{orderId}/meta"


async def market_get_orders_metadata_obtain(orderId):

    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL.format(orderId=orderId)) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = 5632423

    pprint.pp(asyncio.run(market_get_orders_metadata_obtain(sample_data)))
