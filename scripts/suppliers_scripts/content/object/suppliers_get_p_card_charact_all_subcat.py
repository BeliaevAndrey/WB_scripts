"""
Характеристики для создания КТ по всем подкатегориям
https://openapi.wildberries.ru/#tag/Kontent-Konfigurator/paths/~1content~1v1~1object~1characteristics~1list~1filter/get

С помощью данного метода можно получить список характеристик,
которые можно или нужно заполнить при создании КТ в подкатегории
определенной родительской категории.
Характеристики с charcType=4, имеющие единственное значение, указывать
строго без массива, в противном случае карточка не будет создана:
Правильно: {"Высота упаковки": 4}
Не правильно: {"Высота упаковки": [4]}
Query Parameters
name    string      Example: name=Косухи        Поиск по родительской категории.

Responses
200
{
  "data": [
    {
      "objectName": "Косухи",
      "name": "Особенности модели",
      "required": false,
      "unitName": "",
      "maxCount": 1,
      "popular": false,
      "charcType": 1
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

import asyncio

import aiohttp

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/content/v1/object/characteristics/list/filter"


async def a_get_supp_product_category_all(name: str = '') -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
        'name': name,
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    pprint.pp(asyncio.run(a_get_supp_product_category_all()))
