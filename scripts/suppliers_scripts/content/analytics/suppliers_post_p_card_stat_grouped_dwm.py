"""
Получение статистики КТ по дням/неделям/месяцам за период, сгруппированный по предметам, брендам и тегам
https://openapi.wildberries.ru/#tag/Kontent-Analitika/paths/~1content~1v1~1analytics~1nm-report~1grouped~1history/post
Получение статистики КТ по дням/неделям/месяцам за период, сгруппированный по предметам, брендам и тегам.
Поля brandNames, objectIDs, tagIDs могут быть пустыми, тогда группировка происходит по всем карточкам продавца.
В запросе произведение количества предметов, брендов, тегов не должно быть больше 16.

Request samples
{
    "objectIDs": [358],
    "brandNames": ["Some"],
    "tagIDs": [123],
    "period":                   # REQUIRED. --  object    Период
        {
            "begin": "2023-06-21",
            "end": "2023-06-23"
        },
    "timezone": "Europe/Moscow",
    "aggregationLevel": "day"
}

Responses
200
 {
    "data":
        [{
            "object":
                {
                    "id": 358,
                    "name": "Шампуни"
                },
            "brandName": "Some",
            "tag":
                {"id": 123,
                 "name": "Sale"
                 },
            "history": [{...}]
        }],
    "error": true,
    "errorText": "",
    "additionalErrors": [
        {"field": "string", "description": "string"}
    ]
}

400
{
  "data": null,
  "error": true,
  "errorText": "Текст ошибки",
  "additionalErrors": [
    {
      "field": "string",
      "description": "string"
    }
  ]
}
401 "proxy: unauthorized"

403
{ "data": null,
  "error": true,
  "errorText": "Доступ запрещен",
  "additionalErrors": "Доступ запрещен"
}
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL_1 = "https://suppliers-api.wildberries.ru/content/v1/analytics/nm-report/grouped/history"
URL_2 = "https://suppliers-api.wb.ru/content/v1/analytics/nm-report/grouped/history"


async def a_get_supp_pc_stat_grouped_dwm(period: dict, **kwargs) -> tuple | dict:

    headers_dict = {
        "Authorization": __token,
    }

    params = {
        'period': period,
    }

    if kwargs:
        params.update(kwargs)

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL_1, json=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    period = {
        "begin": "2023-06-21",
        "end": "2023-06-23"
    }

    pprint.pp(asyncio.run(a_get_supp_pc_stat_grouped_dwm(period=period)))
