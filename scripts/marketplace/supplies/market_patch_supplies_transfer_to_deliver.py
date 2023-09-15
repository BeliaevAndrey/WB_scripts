"""
Передать поставку в доставку
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies~1{supplyId}~1deliver/patch

Закрывает поставку и переводит все сборочные задания в ней в статус complete ("В доставке").
После закрытия поставки новые сборочные задания к ней добавить будет невозможно.
Передать поставку в доставку можно только при наличии в ней хотя бы одного сборочного
задания и отсутствии пустых коробов.

Path Parameters
supplyId (REQUIRED) -- string -- Example: WB-GI-1234567 -- ID поставки


Responses samples
204 -- Передано

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

URL = "https://suppliers-api.wildberries.ru/api/v3/supplies/{supplyId}/deliver"


async def market_patch_supplies_transfer_to_deliver(supplyId: str) -> str | tuple:
    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.patch(url=URL.format(supplyId=supplyId)) as response:
            if response.status == 204:
                return await response.text()
            else:
                return response.status, await response.text()

if __name__ == '__main__':
    import pprint
    data = {
        "supplyId": "WB-GI-test567",
    }
    pprint.pp(asyncio.run(market_patch_supplies_transfer_to_deliver(**data)))
