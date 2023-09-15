"""
Получить информацию о поставке
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies~1{supplyId}/get

Возвращает информацию о поставке

Path Parameters
supplyId (REQUIRED) -- string -- Example: WB-GI-1234567 -- ID поставки

Responses samples
200
{
  "id": "WB-GI-1234567",
  "done": true,
  "createdAt": "2022-05-04T07:56:29Z",
  "closedAt": "2022-05-04T07:56:29Z",
  "scanDt": "2022-05-04T07:56:29Z",
  "name": "Тестовая поставка",
  "isLargeCargo": true
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

URL = "https://suppliers-api.wildberries.ru/api/v3/supplies/{supplyId}"


async def market_get_supplies_info_by_id(supplyId: str) -> dict | tuple:
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
    pprint.pp(asyncio.run(market_get_supplies_info_by_id(**data)))
