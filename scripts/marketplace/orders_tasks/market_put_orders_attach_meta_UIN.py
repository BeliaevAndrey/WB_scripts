"""
Закрепить за сборочным заданием УИН (уникальный идентификационный номер)
https://openapi.wildberries.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1{orderId}~1meta~1uin/put

Обновляет УИН сборочного задания. У одного сборочного задания может быть только один УИН.
Добавлять маркировку можно только для заказов в статусе confirm.

Path Parameters
orderId(REQUIRED) -- integer <int64> -- ID сборочного задания

Request Body schema: application/json
uin (REQUIRED) -- string = 16 characters -- УИН

Request samples:
{
  "uin": "1234567890123456"
}

Response Samples:
204 -- Обновлено
401 -- ошибка авторизации
403 -- доступ запрещен
409 -- ошибка обновления метаданных
429 -- превышен лимит по запросам
500 -- ошибка сервера
"""
from __future__ import annotations

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/orders/{orderId}/meta/uin"


async def market_put_orders_attach_meta_uin(orderId, data):

    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.put(url=URL.format(orderId=orderId), json=data) as response:
            if response.status == 204:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    order_id = 5632423
    sample_data = {"uin": "1234567890123456"}

    pprint.pp(asyncio.run(market_put_orders_attach_meta_uin(order_id, sample_data)))
