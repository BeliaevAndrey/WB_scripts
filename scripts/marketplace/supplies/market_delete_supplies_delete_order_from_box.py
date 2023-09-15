"""
Удалить заказ из короба
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies~1{supplyId}~1trbx~1{trbxId}~1orders~1{orderId}/delete

Удаляет заказ из короба выбранной поставки.
Можно удалить, только пока поставка на сборке.

path Parameters
supplyId (REQUIRED) -- string -- ID поставки
trbxId (REQUIRED) -- string -- ID короба
orderId (REQUIRED) -- integer <int64> -- ID сборочного задания


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

URL = "https://suppliers-api.wildberries.ru/api/v3/supplies/{supplyId}/trbx/{trbxId}/orders/{orderId}"


async def market_delete_supplies_delete_order_from_box(supplyId: str, trbxId: str, orderId: int) -> tuple:

    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.delete(url=URL.format(
                supplyId=supplyId, trbxId=trbxId, orderId=orderId)) as response:
            if response.status != 204:
                return response.status, await response.text()
            else:
                return response.status,


if __name__ == '__main__':
    import pprint

    sample_data = {
        "supplyId": "WB-GI-57989471",
        "trbxId": "WB-TRBX-1234567",
        "orderId": 1234567
    }

    pprint.pp(asyncio.run(market_delete_supplies_delete_order_from_box(**sample_data)))
