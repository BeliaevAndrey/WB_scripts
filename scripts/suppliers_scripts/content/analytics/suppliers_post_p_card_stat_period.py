"""
Получение статистики КТ за выбранный период, по nmID/предметам/брендам/тегам
https://openapi.wildberries.ru/#tag/Kontent-Analitika/paths/~1content~1v1~1analytics~1nm-report~1detail/post

Request samples
{
  "brandNames": ["Some"],
  "objectIDs": [358],
  "tagIDs": [123],
  "nmIDs": [1234567],
  "timezone": "Europe/Moscow",
  "period": {                           # REQUIRED  -- Период
    "begin": "2023-06-01 20:05:32",
    "end": "2023-06-26 20:05:32"
  },
  "orderBy": {
    "field": "ordersSumRub",
    "mode": "asc"
  },
  "page": 1                              # REQUIRED  -- integer <int32> Страница

}

Responses
200
{
        "data":
            {
                "page": 1,
                "isNextPage": True,
                "cards":
                    [
                        {
                            "nmID": 1234567,
                            "vendorCode": "supplierVendor",
                            "brandName": "Some",
                            "tags": [{...}],
                            "object": {...},
                            "statistics": {...},
                            "stocks": {...}
                        }
                    ]

            },
        "error": True,
        "errorText": "",
        "additionalErrors":
            [{
                "field": "string",
                "description": "string"
            }]
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

URL_1 = "https://suppliers-api.wildberries.ru/content/v1/analytics/nm-report/detail"
URL_2 = "https://suppliers-api.wb.ru/content/v1/analytics/nm-report/detail"


async def a_get_supp_pc_stats_period(period: dict, page: int = 1, **kwargs) -> tuple | dict:
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
    period = {
        "begin": "2023-06-01 20:05:32",
        "end": "2023-06-26 20:05:32"
    }
    pprint.pp(asyncio.run(a_get_supp_pc_stats_period(period=period, page=1, nmIDs=[163868337, 165779176])))
