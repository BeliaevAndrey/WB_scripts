"""
Создать новую поставку
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies/post

Ограничения работы с поставками:

* Только для сборочных заданий по схеме "Везу на склад WB"
* При добавлении в поставку все передаваемые сборочные задания в статусе
        new ("Новое") будут автоматически переведены в статус confirm ("На сборке").
* Обратите внимание, что если вы переведёте сборочное задание в статус
        cancel ("Отмена продавцом"), то сборочное задание автоматически
        удалится из поставки, если было прикреплено к ней.
* Поставку можно собрать только из одного типа сборочных заданий:
        сКГТ (isLargeCargo = true) или обычный (isLargeCargo = false).
        Новая поставка не обладает сКГТ-признаком.
        При добавлении первого заказа в поставку она приобретает сКГТ-признак
        добавляемого товара в заказе.

Request Body schema: application/json
name -- string [ 1 .. 128 ] characters -- Наименование поставки

Request samples
{
  "name": "Тестовая поставка"
}

Response Schema: application/json
id -- string -- Идентификатор поставки

Response samples
201
{"id": "WB-GI-1234567"}

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

URL = "https://suppliers-api.wildberries.ru/api/v3/supplies"


async def market_post_supplies_create_new(data: dict) -> list[list[dict]] | tuple:

    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=data) as response:
            if response.status == 201:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    data = {"name": "Тестовая поставка"}

    pprint.pp(asyncio.run(market_post_supplies_create_new(data)))
