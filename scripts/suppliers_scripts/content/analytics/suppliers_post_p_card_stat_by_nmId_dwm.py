"""
Получение статистики КТ по дням/неделям/месяцам по выбранным nmID
https://openapi.wildberries.ru/#tag/Kontent-Analitika/paths/~1content~1v1~1analytics~1nm-report~1detail~1history/post

Request samples
{
  "nmIDs": [                    # REQUIRED  -- int array    Артикул WB (max. 20)
    1234567
  ],
  "period": {                   # REQUIRED  -- object   Период
    "begin": "2023-06-20",
    "end": "2023-06-22"
  },
  "timezone": "Europe/Moscow",
  "aggregationLevel": "day"
}

Responses
200
 {

    "data":
    [{
        "nmID": 1234567,
        "imtName": "Наименование КТ",
        "vendorCode": "supplierVendor",
        "history":
            [
                {
                    "dt": "2023-06-20",
                    "openCardCount": 26,
                    "addToCartCount": 1,
                    "ordersCount": 0,
                    "ordersSumRub": 0,
                    "buyoutsCount": 0,
                    "buyoutsSumRub": 0,
                    "buyoutPercent": 0,
                    "addToCartConversion": 3.8,
                    "cartToOrderConversion": 0
                }
            ]
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

URL_1 = "https://suppliers-api.wildberries.ru/content/v1/analytics/nm-report/detail/history"
URL_2 = "https://suppliers-api.wb.ru/content/v1/analytics/nm-report/detail/history"


async def a_get_supp_pc_stats_period(period: dict, nmIDs: list[int], **kwargs) -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
        'period': period,
        'nmIDs': nmIDs,
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

    sample_period = {
        "begin": "2023-06-01",
        "end": "2023-06-26"
    }

    req_params_example = {
        "nmIDs": [163868337],
        "period":
            {
                "begin": "2023-06-20",
                "end": "2023-06-22"
            },
        "timezone": "Europe/Moscow",
        "aggregationLevel": "day"

    }
    pprint.pp(asyncio.run(a_get_supp_pc_stats_period(**req_params_example)))
    # pprint.pp(asyncio.run(a_get_supp_pc_stats_period(period=sample_period, nmIDs=[163868337])))
