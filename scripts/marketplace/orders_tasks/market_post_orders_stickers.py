"""
Получить этикетки для сборочных заданий
https://openapi.wildberries.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1stickers/post
Возвращает список этикеток по переданному массиву сборочных заданий.
Можно запросить этикетку в формате svg, zplv (вертикальный), zplh (горизонтальный), png.

Ограничения при работе с методом:
Нельзя запросить больше 100 этикеток за раз (не более 100 идентификаторов сборочных заданий в запросе).
Метод возвращает этикетки только для сборочных заданий, находящихся на сборке (в статусе confirm).
Доступные размеры:
    580x400 пикселей, при параметрах width = 58, height = 40
    400x300 пикселей, при параметрах width = 40, height = 30

query Parameters
type(REQUIRED) -- string Enum: "svg" "zplv" "zplh" "png" -- Тип этикетки
width -- (REQUIRED) -- integer Enum: 58 40 -- Ширина этикетки
height(REQUIRED) -- integer Enum: 40 30 -- Высота этикетки


Request Body schema: application/json
orders -- Array of integers <int64> [ 1 .. 100 ] items [ items <int64 > ] -- Массив идентификаторов сборочных заданий


Response Schema: application/json
200
Stickers -- Array of objects
[
orderId -- integer <int64> -- Идентификатор сборочного задания
partA -- integer -- Первая часть идентификатора этикетки (для печати подписи)
partB -- integer -- Вторая часть идентификатора этикетки
barcode -- string -- Закодированное значение этикетки
file -- string <byte> -- Полное представление этикетки в заданном формате. (кодировка base64)
]

400
{"code": "IncorrectParameter", "message": "Передан некорректный параметр"}
or
{"code": "IncorrectRequestBody", "message": "Некорректное тело запроса"}
or
{"code": "IncorrectRequest", "message": "Переданы некорректные данные"}

401 -- ошибка авторизации
403 -- доступ запрещен
500 -- ошибка сервера
"""
from __future__ import annotations

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/orders/stickers"


async def market_post_orders_stickers(data: dict[str, list[int]]):
    """
    data: list[int]  -- Array of integers <int64> [1 .. 1000] -- items [items<int64 >] Список идентификаторов сборочных заданий
    :param data: data = {"orders": [int]}
    :return:
    """

    headers_dict = {
        'Authorization': __token
    }
    params = {
        "type": data.get("type"),
        "width": data.get("width"),
        "height": data.get("height")
    }
    payload = {
        "orders": data.get("orders")
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, params=params, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "orders": [5632423],
        "type": "svg",
        "width": 40,
        "height": 30,
    }

    pprint.pp(asyncio.run(market_post_orders_stickers(sample_data)))
