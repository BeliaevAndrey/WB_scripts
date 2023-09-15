"""
Категория товаров
https://openapi.wildberries.ru/#tag/Kontent-Konfigurator/paths/~1content~1v1~1object~1all/get

Query Parameters
name    string      Example: name=3D    Поиск по названию категории
top     integer     Example: top=50     Количество запрашиваемых значений


Responses
200
 {
  "data": [
    {
      "objectID": 2560,
      "parentID": 479,
      "objectName": "3D очки",
      "parentName": "Электроника",
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

URL = "https://suppliers-api.wildberries.ru/content/v1/object/all"


async def a_get_supp_product_category(name: str, amount: int) -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
        'name': name,
        'top': amount,
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    print(asyncio.run(a_get_supp_product_category("", 10000)))
