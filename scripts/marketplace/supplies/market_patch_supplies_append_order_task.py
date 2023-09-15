"""
Добавить к поставке сборочное задание
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies~1{supplyId}~1orders~1{orderId}/patch

Добавляет к поставке сборочное задание и переводит его в статус confirm ("На сборке").
Также может перемещать сборочное задание между активными поставками, либо из закрытой в
активную при условии, что сборочное задание требует повторной отгрузки.
Добавить в поставку возможно только задания с соответствующим сКГТ-признаком (isLargeCargo),
либо если поставке ещё не присвоен сКГТ-признак (isLargeCargo = null).

Path Parameters
supplyId (REQUIRED) -- string -- Example: WB-GI-1234567 -- ID поставки
orderId (REQUIRED) -- integer <int64> -- ID сборочного задания


Responses samples
204 -- закреплено за поставкой
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

URL = "https://suppliers-api.wildberries.ru/api/v3/supplies/{supplyId}/orders/{orderId}"


async def market_patch_supplies_append_order_task(supplyId: str, orderId: int) -> str | tuple:
    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.patch(url=URL.format(supplyId=supplyId, orderId=orderId)) as response:
            if response.status == 204:
                return await response.text()
            else:
                return response.status, await response.text()

if __name__ == '__main__':
    import pprint
    data = {
        "supplyId": "WB-GI-57989471",
        "orderId": 5632423
    }
    pprint.pp(asyncio.run(market_patch_supplies_append_order_task(**data)))
