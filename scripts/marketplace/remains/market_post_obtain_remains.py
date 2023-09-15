"""
Получить остатки товаров
https://openapi.wildberries.ru/#tag/Marketplace-Ostatki/paths/~1api~1v3~1stocks~1{warehouseId}/post

Возвращает остатки товаров.

Допускается максимум 300 запросов в минуту на методы Marketplace в целом

path Parameters
warehouseId(REQUIRED) -- integer <int64> -- ID склада продавца

Request Body schema: application/json
skus -- Array of strings -- Массив баркодов

Request sample
{
  "skus": ["BarcodeTest123"]
}

Responses
200     -- Список остатков
Response Schema: application/json
stocks -- Array of objects
Array [
sku -- string -- Баркод
amount -- integer -- Остаток
]

Response sample
{
"stocks": [
    { "sku": "BarcodeTest123",
      "amount": 10}]
      }

400 -- Запрос содержит некорректные данные
401 -- ошибка авторизации
403 -- доступ запрещен
404 -- ресурс не найден
409 -- ошибка обновления
429 -- превышен лимит запросов
500 -- ошибка сервера
"""

from __future__ import annotations

import aiohttp
import asyncio
import json

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouseId}"


async def market_put_renew_remains(warehouseId: int, skus: list[str ]):
    headers_dict = {
        "Authorization": __token
    }
    payload = {
        "skus": skus
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.put(url=URL.format(warehouseId=warehouseId),
                               json=payload) as response:
            if response.status != 204:
                return response.status, await response.text()
            else:
                return response.status


if __name__ == '__main__':
    sample_warehouseId = 1
    sample_req = ["BarcodeTest123"]

    print(asyncio.run(market_put_renew_remains(sample_warehouseId, sample_req)))
