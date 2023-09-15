"""
Характеристики для создания КТ для категории товара
https://openapi.wildberries.ru/#tag/Kontent-Konfigurator/paths/~1content~1v1~1object~1characteristics~1{objectName}/get

Важно: обязательная к заполнению характеристика при создании карточки любого товара - Предмет.
Значение характеристики Предмет соответствует значению параметра objectName в запросе.

Характеристики с charcType=4, имеющие единственное значение, указывать строго без массива, в противном случае карточка не будет создана:
Правильно:
{"Высота упаковки": 4}
Не правильно:
{"Высота упаковки": [4]}


Query Parameters
objectName  required    string      Example: Носки  Поиск по наименованию категории

Responses
200
{
  "data": [
    {
      "objectName": "Носки",
      "name": "Глубина упаковки",
      "required": false,
      "unitName": "см",
      "maxCount": 0,
      "popular": false,
      "charcType": 4
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

URL = "https://suppliers-api.wildberries.ru/content/v1/object/characteristics/{objectName}"


async def a_get_supp_product_category_subcat(object_name: str) -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL.format(objectName=object_name), params=params) as response:
            print(f'{response.url=}')
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    print(asyncio.run(a_get_supp_product_category_subcat("Носки")))
