"""
Страна Производства
https://openapi.wildberries.ru/#tag/Kontent-Konfigurator/paths/~1content~1v1~1directory~1countries/get

Responses
200
{
  "data": [
    {
      "name": "Афганистан",
      "fullName": "Исламский Эмират Афганистан"
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

URL = "https://suppliers-api.wildberries.ru/content/v1/directory/countries"


async def a_get_supp_p_card_country_orig() -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
        "name": "Афганистан"
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    pprint.pp(asyncio.run(a_get_supp_p_card_country_orig()))
