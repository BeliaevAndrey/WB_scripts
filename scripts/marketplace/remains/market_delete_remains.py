"""
Удалить остатки товаров
https://openapi.wildberries.ru/#tag/Marketplace-Ostatki

Допускается максимум 300 запросов в минуту на методы Marketplace в целом

Удаляет остатки товаров.
ВНИМАНИЕ! ДЕЙСТВИЕ НЕОБРАТИМО. Удаленный остаток будет необходимо загрузить
повторно для возобновления продаж.

Path Parameters
warehouseId(REQUIRED) -- integer <int64> -- ID склада продавца

Request Body schema: application/json
skus -- Array of strings [ 1 .. 1000 ] items -- Массив баркодов

Request sample
{
    "skus": ["BarcodeTest123"]
}

Responses
204 -- удалено
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


async def market_delete_remains(warehouseId: int, skus: list[dict]):
    headers_dict = {
        "Authorization": __token
    }
    payload = {
        "skus": skus
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.delete(url=URL.format(warehouseId=warehouseId),
                                  json=payload) as response:
            if response.status != 204:
                return response.status, await response.text()
            else:
                return response.status


if __name__ == '__main__':
    sample_warehouseId = 1
    sample_req = [
        {"skus": ["BarcodeTest123"]}
    ]
    print(asyncio.run(market_delete_remains(sample_warehouseId, sample_req)))
