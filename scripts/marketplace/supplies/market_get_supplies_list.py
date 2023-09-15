"""
Получить список поставок
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies/get

Query Parameters

limit(REQUIRED) -- integer [ 1 .. 1000 ] -- Параметр пагинации. Устанавливает предельное количество возвращаемых данных.
next (REQUIRED) -- integer <int64> -- Параметр пагинации. Устанавливает значение,
                                      с которого надо получить следующий пакет данных.
                                      Для получения полного списка данных должен быть равен 0
                                      в первом запросе. Для следующих запросов необходимо брать
                                      значения из одноимённого поля в ответе.

Responses samples
200
{ "next": 0,
  "supplies":
  [{ "id": "WB-GI-1234567",
      "done": true,
      "createdAt": "2022-05-04T07:56:29Z",
      "closedAt": "2022-05-04T07:56:29Z",
      "scanDt": "2022-05-04T07:56:29Z",
      "name": "Тестовая поставка",
      "isLargeCargo": true
    }]}

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


async def market_get_supplies_list(data: dict,
                                   responses: list = None
                                   ) -> list[list[dict]] | tuple:
    """
    data = {
        limit: <integer> [1 ... 1000]
        next: <integer64>
    }
    :param responses: list[dict]    -- list of responses
    :param data: dict[str, int]     -- request data
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
                responses.append(tmp["supplies"])
                new_next = tmp.get("next")
                if new_next > 0:
                    new_data = {
                        "limit": 1000,
                        "next": new_next
                    }
                    return await market_get_supplies_list(new_data, responses)
                else:
                    return responses
            else:
                return response.status, await response.text()

if __name__ == '__main__':
    import pprint
    data = {
        "limit": 1000,
        "next": 0
    }
    pprint.pp(asyncio.run(market_get_supplies_list(data)))
