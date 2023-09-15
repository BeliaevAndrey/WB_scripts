"""
Получение КТ по артикулам продавца
https://openapi.wildberries.ru/#tag/Kontent-Prosmotr/paths/~1content~1v1~1cards~1filter/post

Метод позволяет получить полную информацию по КТ с помощью артикула(-ов) продавца.

Request Body schema: application/json

vendorCodes -- Array of strings -- Массив артикулов продавца. Максимальное количество в запросе 100.

allowedCategoriesOnly -- boolean
true - показать КТ только из разрешенных к реализации категорий
false - показать КТ из всех категорий

Request sample

{
  "vendorCodes": [
    "6000000001"
  ],
  "allowedCategoriesOnly": true
}


Response Samples
200
 {
    "data":
        [{"imtID": 9876545135,
          "object": "Рубашки рабочие",
          "objectID": 6165,
          "nmID": 7986515498,
          "vendorCode": "vendorCode",
          "mediaFiles": [...],
          "sizes": [...],
          "characteristics": [],
          "isProhibited": false,
          "tags": [...]}],
    "error": false,
    "errorText": "",
    "additionalErrors": null
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

401
proxy: unauthorized

403
{
  "data": null,
  "error": true,
  "errorText": "Доступ запрещен",
  "additionalErrors": "Доступ запрещен"
}
"""

from __future__ import annotations
import aiohttp
import asyncio
from typing import Any

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/content/v1/cards/filter"


async def a_supp_post_p_card_get_card_by_seller_art(data: dict) -> dict | tuple:
    headers_dict = {
        'Authorization': __token,
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=data) as request:
            if request.status == 200:
                return await request.json()
            else:
                return request.status, await request.text()


if __name__ == '__main__':
    import pprint

    sample_req = {
        "vendorCodes": ["6000000001"],
        "allowedCategoriesOnly": True
    }

    pprint.pp(asyncio.run(a_supp_post_p_card_get_card_by_seller_art(sample_req)))
