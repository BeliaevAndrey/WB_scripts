"""
Список тегов
https://openapi.wildberries.ru/#tag/Kontent-Tegi/paths/~1content~1v1~1tags/get
Метод позволяет получить список существующих тегов продавца.

Responses
200
{
  "data": [
    {
      "id": 1,
      "color": "D1CFD7",
      "name": "Sale"
    }
  ],
  "error": false,
  "errorText": "",
  "additionalErrors": ""
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

URL = "https://suppliers-api.wildberries.ru/content/v1/tags"


async def a_get_supp_p_card_tags_list() -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    print(asyncio.run(a_get_supp_p_card_tags_list()))
