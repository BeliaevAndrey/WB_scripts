"""
Получение статистики КТ за период, сгруппированный по предметам, брендам и тегам
https://openapi.wildberries.ru/#tag/Kontent-Analitika/paths/~1content~1v1~1analytics~1nm-report~1grouped/post
Получение статистики КТ за период, сгруппированный по предметам, брендам и тегам.
Поля brandNames, objectIDs, tagIDs могут быть пустыми, тогда группировка происходит по всем карточкам продавца.

Request samples
{
  "objectIDs": [358],
  "brandNames": ["Some"],
  "tagIDs": [123],
  "timezone": "Europe/Moscow",
  "period": {                       # REQIURED  -- object Период
    "begin": "2023-03-01 20:05:32",
    "end": "2023-06-26 20:05:32"
    },
  "orderBy": {
    "field": "ordersSumRub",
    "mode": "asc"
    },
  "page": 1                         # REQUIRED  -- integer <int32> Страница
}

Responses
200
 {
    "data":
    {
        "page": 1,
        "isNextPage": true,
        "groups":
            [{
                "brandName": "Some",
                "tags":
                [{
                    "id": 123,
                    "name": "Sale"
                }],
            "object":
            {
                "id": 1668,
                "name": "Воски для волос"
            },
            "statistics":
            {
                "selectedPeriod": {...},
                "previousPeriod": {...},
                "periodComparison": {...}
                }
            }]
    },
    "error": true,
    "errorText": "",
    "additionalErrors": []
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

URL_1 = "https://suppliers-api.wildberries.ru/content/v1/analytics/nm-report/grouped"
URL_2 = "https://suppliers-api.wb.ru/content/v1/analytics/nm-report/grouped"


async def a_get_supp_pc_stat_grouped(period: dict, page: int = 1, **kwargs) -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
        'period': period,
        'page': page,
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

    # period = {
    #     "begin": "2023-06-01 20:05:32",
    #     "end": "2023-06-26 20:05:32"
    # }

    req_params_example = {
        "objectIDs": [],
        "brandNames": [],
        "tagIDs":
            [],
        "timezone": "Europe/Moscow",
        "period":
            {
                "begin": "2023-03-01 20:05:32",
                "end": "2023-06-26 20:05:32"
            },
        "orderBy": {"field": "ordersSumRub", "mode": "asc"},
        "page": 1}
    pprint.pp(asyncio.run(a_get_supp_pc_stat_grouped(**req_params_example)))
