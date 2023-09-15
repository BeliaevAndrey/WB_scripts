"""
Получить информацию по сборочным заданиям
https://openapi.wildberries.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders/get
Возвращает информацию по сборочным заданиям без их актуального статуса.
Данные по сборочному заданию, возвращающиеся в данном методе, не меняются.
Рекомендуется использовать для получения исторических данных.

query Parameters
limit(REQUIRED) -- integer [ 1 .. 1000 ] -- Параметр пагинации. Устанавливает
                                            предельное количество возвращаемых данных.
next(REQUIRED) -- integer <int64> -- Параметр пагинации. Устанавливает значение,
                                     с которого надо получить следующий пакет данных.
                                     Для получения полного списка данных должен быть равен 0 в
                                     первом запросе. Для следующих запросов необходимо брать
                                     значения из одноимённого поля в ответе.
dateFrom -- integer -- Дата начала периода в формате Unix timestamp. Необязательный параметр.
dateTo -- integer -- Дата конца периода в формате Unix timestamp. Необязательный параметр.


Response Schema: application/json
200
next    --  integer <int64> (Next)   -- Параметр пагинации.
                                        Содержит значение, которое необходимо
                                        указать в запросе для получения следующего пакета данных

orders  --  Array of objects (Order) -- Список новых сборочных заданий

401 -- ошибка авторизации
403 -- доступ запрещен
429 -- превышен лимит по запросам
500 -- ошибка сервера
"""
from __future__ import annotations

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/orders"


async def market_get_orders_info(data: dict,
                                 responses: list = None,
                                 ) -> list[list[dict]] | tuple:
    """
        data = {
        limit: <integer> [1 ... 1000]
        next: <integer64>
        dateFrom: int <Unix Timestamp>
        dateTo: int <Unix Timestamp>
    }
    :param data: dict[str, int]
    :param responses: list[list]
    :return:
    """
    headers_dict = {
        'Authorization': __token
    }
    if responses is None:
        responses = []

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=data) as response:
            if response.status == 200:
                tmp = await response.json()
                responses.append(tmp["orders"])
                new_next = tmp.get("next", 0)
                if new_next > 0:
                    new_data = {
                        "limit": 1000,
                        "next": new_next
                    }
                    return await market_get_orders_info(new_data, responses)
                else:
                    return responses
            else:
                return response.status, await response.text()

if __name__ == '__main__':
    import pprint
    from datetime import datetime as _dt
    sample_data = {
        "limit": 1000,
        "next": 0,
        "dateFrom": int(_dt.now().timestamp()),  # optional
        "dateTo": int(_dt.now().timestamp())  # optional
    }
    pprint.pp(asyncio.run(market_get_orders_info(sample_data)))
