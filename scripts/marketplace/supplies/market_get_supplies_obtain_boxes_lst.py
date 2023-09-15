"""
Получить список коробов поставки
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies~1{supplyId}~1trbx/get

Возвращает список коробов и идентификаторы заказов, входящих в них.

Path Parameters
supplyId (REQUIRED) -- string -- Example: WB-GI-1234567 -- ID поставки

query Parameters
type(REQUIRED) -- string Enum: "svg" "zplv" "zplh" "png" - Тип этикетки


Responses samples
200
{ "trbxes": [{"id": "WB-TRBX-1234567",
              "orders": [1234567]}]
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

URL = "https://suppliers-api.wildberries.ru/api/v3/supplies/{supplyId}/trbx"


async def market_get_supplies_obtain_boxes_lst(supplyId: str) -> dict | tuple:
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
    pprint.pp(asyncio.run(market_get_supplies_obtain_boxes_lst(**data)))
