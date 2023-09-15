"""
Добавить короба к поставке
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies~1{supplyId}~1trbx/post

Добавляет требуемое количество коробов в поставку.
Можно добавить, только пока поставка на сборке.


path Parameters
supplyId (REQUIRED) -- string -- ID поставки

Request Body schema: application/json
amount(REQUIRED) -- integer [ 1 .. 1000 ] -- Количество коробов, которые необходимо добавить к поставке.

Request samples
{"amount": 4}

Response Schema: application/json
trbxIds -- Array of strings >= 1 -- Список ID коробов, которые были созданы.

Response samples
201
{"trbxIds": ["WB-TRBX-1234567"]}

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

409
 '{"code":"FailedToAddSupplyTrbx","message":"Не удалось добавить коробку. '
 'Убедитесь, что поставка удовлетворяет всем необходимым требованиям."}')

429 -- превышен лимит по запросам

500
{ "code": "InternalServerError",
  "message": "Внутренняя ошибка сервиса"}
"""
from __future__ import annotations

import aiohttp
import asyncio
import json

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/supplies/{supplyId}/trbx"


async def market_post_supplies_append_boxes(supplyId: int, amount: int) -> dict[str, list[str]] | tuple:

    headers_dict = {
        'Authorization': __token
    }

    data = {
        "amount": amount
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL.format(supplyId=supplyId), json=data) as response:
            if response.status == 201:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "supplyId": "WB-GI-57989471",
        "amount": 4
    }

    pprint.pp(asyncio.run(market_post_supplies_append_boxes(**sample_data)))
