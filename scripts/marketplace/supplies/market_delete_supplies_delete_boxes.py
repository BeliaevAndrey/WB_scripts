"""
Удалить короба из поставки
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies~1{supplyId}~1trbx/delete

Убирает заказы из перечисленных коробов поставки и удаляет короба.
Можно удалить, только пока поставка на сборке.


path Parameters
supplyId (REQUIRED) -- string -- ID поставки

Request Body schema: application/json
trbxIds (REQUIRED) -- Array of strings -- Список ID коробов, которые необходимо удалить.


Request samples
{
  "trbxIds": ["WB-TRBX-1234567"]
}


Response samples
204 -- удалено

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


async def market_delete_supplies_delete_boxes(supplyId: int, trbxIds: list[str]) -> tuple:

    headers_dict = {
        'Authorization': __token
    }

    data = {
        "trbxIds": trbxIds
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.delete(url=URL.format(supplyId=supplyId), data=data) as response:
            if response.status == 204:
                return response.status, await response.text()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "supplyId": "WB-GI-57989471",
        "trbxIds": "WB-TRBX-1234567"
    }

    pprint.pp(asyncio.run(market_delete_supplies_delete_boxes(**sample_data)))
