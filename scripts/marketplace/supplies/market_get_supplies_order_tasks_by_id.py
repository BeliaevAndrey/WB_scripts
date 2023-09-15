"""
Получить сборочные задания в поставке
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies~1{supplyId}~1orders/get

Возвращает сборочные задания, закреплённые за поставкой.

Path Parameters
supplyId (REQUIRED) -- string -- Example: WB-GI-1234567 -- ID поставки


Response Schema: application/json
orders -- Array of objects (SupplyOrder)

Responses samples
200
{"orders": [{
    "id": 13833711,
    "rid": "f884001e44e511edb8780242ac120002",
    "createdAt": "2022-05-04T07:56:29Z",
    "warehouseId": 658434,
    "offices": [...],
    "user": {...},
    "skus": [...],
    "price": 0,
    "convertedPrice": 0,
    "currencyCode": 0,
    "convertedCurrencyCode": 0,
    "orderUid": "string",
    "nmId": 0,
    "chrtId": 0,
    "article": "one-ring-7548",
    "isLargeCargo": true}]
}

400
{ "code": "IncorrectParameter",
  "message": "Передан некорректный параметр"}

401
proxy: unauthorized     -- Токен отсутствует
or
proxy: invalid token    -- Токен недействителен
or
proxy: not found        -- Токен удален

403
{ "code": "AccessDenied",
  "message": "Доступ запрещён"}
404
{ "code": "NotFound",
  "message": "Не найдено"}
409
{ "code": "FailedToAddSupplyOrder",
  "message": "Не удалось закрепить сборочное задание за поставкой.
  Убедитесь, что сборочное задание и поставка удовлетворяют всем необходимым требованиям."}
500
{ "code": "InternalServerError",
  "message": "Внутренняя ошибка сервиса"}
"""
from __future__ import annotations

import aiohttp
import asyncio
import json

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/supplies/{supplyId}/orders"


async def market_get_supplies_order_tasks_by_id(supplyId: str) -> dict | tuple:
    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL.format(supplyId=supplyId)) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()

if __name__ == '__main__':
    import pprint
    data = {
        "supplyId": "WB-GI-57989471",
    }
    pprint.pp(asyncio.run(market_get_supplies_order_tasks_by_id(**data)))
