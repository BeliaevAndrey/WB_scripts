"""
Создание тега
https://openapi.wildberries.ru/#tag/Kontent-Tegi/paths/~1content~1v1~1tag/post
Метод позволяет создать тег.
Завести можно 8 тегов.
Максимальная длина тега 15 символов.

Request Body schema: application/json
color   string  Цвет тега.
    Доступные цвета:
        D1CFD7 - серый; FEE0E0 - красный; ECDAFF - фиолетовый;
        E4EAFF - синий; DEF1DD - зеленный; FFECC7 - желтый

name    string      Имя тега

Request samples
{
  "color": "D1CFD7",
  "name": "Sale"
}

Responses
200
{
  "data": null,
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

URL = "https://suppliers-api.wildberries.ru/content/v1/tag"


async def a_post_tag_create(color: str, name: str) -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
        "color": color,
        "name": name,
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
        "color": "D1CFD7",
        "name": "Sale",
    }

    pprint.pp(asyncio.run(a_post_tag_create(**sample_req)))
