"""
Добавить заказы к коробу
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies~1{supplyId}~1trbx~1{trbxId}/patch

Добавляет заказы в короб для выбранной поставки.
Можно добавить, только пока поставка на сборке.

Path Parameters
supplyId (REQUIRED) -- string -- Example: WB-GI-1234567 -- ID поставки
trbxId (REQUIRED) -- string -- ID короба

Request Body schema: application/json
orderIds (required) -- Array of integers -- Список заказов, которые необходимо добавить в короб.

Request sample
{"orderIds": [1234567]}

Responses samples
204 -- добавлено
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

URL = "https://suppliers-api.wildberries.ru/api/v3/supplies/{supplyId}/trbx/{trbxId}"


async def market_patch_supplies_append_orders_to_box(supplyId: str,
                                                     trbxId: str,
                                                     payload: dict) -> str | tuple:
    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.patch(url=URL.format(supplyId=supplyId, trbxId=trbxId),
                                 json=payload
                                 ) as response:
            if response.status == 204:
                return await response.text()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    data = {
        "supplyId": "WB-GI-57989471",
        "trbxId": "WB-TRBX-1234567",
        "payload": {"orderIds": [1234567]}
    }

    pprint.pp(asyncio.run(market_patch_supplies_append_orders_to_box(**data)))
