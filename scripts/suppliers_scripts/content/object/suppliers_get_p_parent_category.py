"""
Родительские категории товаров
https://openapi.wildberries.ru/#tag/Kontent-Konfigurator/paths/~1content~1v1~1object~1parent~1all/get

Responses
200
{
  "data": [
    {
      "name": "Электроника",
      "id": 479,
      "isVisible": true
    }
  ],
  "error": false,
  "errorText": "",
  "additionalErrors": ""
}

400
{
  "data": null,
  "error": true,
  "errorText": "Текст ошибки",
  "additionalErrors": {
    "MoveNmsToTrash": "Bad request"
  }
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

URL = "https://suppliers-api.wildberries.ru/content/v1/object/parent/all"


async def a_get_supp_product_category_parent() -> tuple | dict:
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
    print(asyncio.run(a_get_supp_product_category_parent()))
