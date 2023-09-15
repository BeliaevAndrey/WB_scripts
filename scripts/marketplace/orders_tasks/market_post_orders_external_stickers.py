"""
Получить список ссылок на этикетки для сборочных заданий, которые требуются при кроссбордере
https://openapi.wildberries.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1files~1orders~1external-stickers/post

Возвращает список ссылок на этикетки для сборочных заданий, которые требуются при кроссбордере.

Ограничения при работе с методом:

    Нельзя запросить больше 100 этикеток за раз (не более 100 идентификаторов сборочных заданий в запросе).
    Метод возвращает этикетки только для сборочных заданий, находящихся на сборке (в статусе confirm).

Request Body schema: application/json
orders -- Array of integers <int64> [ 1 .. 100 ] items [ items <int64 > ] -- Массив идентификаторов сборочных заданий


Response Schema: application/json
200
Stickers -- Array of objects
[
orderId -- integer <int64> -- Идентификатор сборочного задания
url -- string -- Ссылка, по которой можно получить этикетку для сборочного задания
]

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

URL = "https://suppliers-api.wildberries.ru/api/v3/files/orders/external-stickers"


async def market_post_orders_stickers(data: dict[str, list[int]]):
    """
    data: list[int]  -- Array of integers <int64> [1 .. 1000] -- items [items<int64 >] Список идентификаторов сборочных заданий
    :param data: data = {"orders": [int]}
    :return:
    """

    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "orders": [5632423],
    }

    pprint.pp(asyncio.run(market_post_orders_stickers(sample_data)))
