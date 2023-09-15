"""
Получить статусы сборочных заданий
https://openapi.wildberries.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1status/post
Возвращает статусы сборочных заданий по переданному списку идентификаторов сборочных заданий.

supplierStatus - статус сборочного задания, триггером изменения которого является сам продавец.
Возможны следующие значения данного поля:

Статус -- Описание -- Как перевести сборочное задание в данный статус
new -- Новое сборочное задание
confirm -- На сборке -- При добавлении сборочного задания к поставке PATCH /api/v3/supplies/{supplyId}/orders/{orderId}
complete -- В доставке -- При переводе в доставку соответствующей поставки PATCH /api/v3/supplies/{supplyId}/deliver
cancel -- Отменено продавцом -- PATCH /api/v3/orders/{orderId}/cancel

wbStatus - статус сборочного задания в системе Wildberries.
Возможны следующие значения данного поля:

    waiting - сборочное задание в работе
    sorted - сборочное задание отсортировано
    sold - сборочное задание получено покупателем
    canceled - отмена сборочного задания
    canceled_by_client - отмена сборочного задания покупателем
    defect - отмена сборочного задания по причине брака
    ready_for_pickup - сборочное задание прибыло на ПВЗ

Request Body schema: application/json

orders-- Array of integers <int64> [ 1 .. 1000 ] items [ items <int64 > ]
Список идентификаторов сборочных заданий

Response Schema: application/json
200

orders  --  Array of objects (Order) -- Список новых сборочных заданий

400
{"code": "IncorrectParameter", "message": "Передан некорректный параметр"}
or
{"code": "IncorrectRequestBody", "message": "Некорректное тело запроса"}
or
{"code": "IncorrectRequest", "message": "Переданы некорректные данные"}

401 -- ошибка авторизации
403 -- доступ запрещен
429 -- превышен лимит по запросам
500 -- ошибка сервера
"""
from __future__ import annotations

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/orders/status"


async def market_post_orders_status(data: dict[str, list[int]]):
    """
    data: list[int]  -- Array of integers <int64> [1 .. 1000] -- items [items<int64 >] Список идентификаторов сборочных заданий
    :param data: data = {"orders": [int]}
    :return:
    """

    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, params=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "orders": [5632423]
    }

    pprint.pp(asyncio.run(market_post_orders_status(sample_data)))
