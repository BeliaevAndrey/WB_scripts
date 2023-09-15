"""
Лимиты по КТ
https://openapi.wildberries.ru/#tag/Kontent-Prosmotr/paths/~1content~1v1~1cards~1limits/get

Responses
200
 {"data":
      {"freeLimits": 1500,
       "paidLimits": 10
     },
    "error": false,
     "errorText": "",
    "additionalErrors": null
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

URL = "https://suppliers-api.wildberries.ru/content/v1/cards/limits"


async def a_get_supp_pc_lims() -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    print(asyncio.run(a_get_supp_pc_lims()))
