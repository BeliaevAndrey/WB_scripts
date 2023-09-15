"""
Список НМ, находящихся в корзине
https://openapi.wildberries.ru/#tag/Kontent-Korzina/paths/~1content~1v1~1cards~1trash~1list/post
Метод позволяет получить список НМ, находящихся в корзине.
Метод позволяет получить список НМ, которые находятся в корзине по фильтру
(баркод (skus),артикул продавца(vendorCode), артикул WB(nmID))
с пагинацией и сортировкой.

Request Body schema: application/json
sourt       object

    sortColumn      string      Поле, по которому будет сортироваться
                                список КТ (пока что поддерживается только updateAt)
    ascending       boolean     Тип сортировки
    searchValue     string      Поле, по которому будет осуществляться поиск:
                                по баркоду(skus),
                                артикулу продавца (vendorCode),
                                артикулу WB (nmID)
    offset          integer     С какого элемента выдавать данные
    limit           integer     Кол-во запрашиваемых КТ (max. 1000)


Request samples
{
    "sort":
        {
            "sortColumn": "updateAt",
            "ascending": false,
            "searchValue": "vendorCodeOne",
            "offset": 0,
            "limit": 50
            }
}

Response samples
200
{
  "data": {
    "cards": [{
        "nmID": 12213123,
        "objectID": 280,
        "vendorCode": "vendorCodeOne",
        "object": "Шляпы",
        "brand": "TestBrandOne",
        "updatedAt": "2022-04-19T15:21:10Z",
        "colors": ["красный"],
        "mediaFiles": ["mediaFileLink1", "mediaFileLink2"],
        "sizes": [{
            "skus": ["barcode001"],
            "techSize": "42",
            "wbSize": "42",
            "price": 2000
          }]
      }],
    "cursor": {
      "offset": 0,
      "limit": 50
    }
  },
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

URL = "https://suppliers-api.wildberries.ru/content/v1/cards/trash/list"


async def a_post_tag_create(sort: dict) -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
        "sort": sort,
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_req = {
        "sort":
            {
                "sortColumn": "updateAt",
                "ascending": False,
                "searchValue": "vendorCodeOne",
                "offset": 0,
                "limit": 50
            }
    }

    pprint.pp(asyncio.run(a_post_tag_create(**sample_req)))
