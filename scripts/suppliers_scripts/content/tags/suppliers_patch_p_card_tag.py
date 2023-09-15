"""
Изменение тега
https://openapi.wildberries.ru/#tag/Kontent-Tegi/paths/~1content~1v1~1tag~1{id}/patch
Метод позволяет изменять информацию о теге (имя и цвет).

path Parameters
id      REQUIRED    integer     Числовой идентификатор тега

Request Body schema: application/json
color   string  Цвет тега.
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

URL = "https://suppliers-api.wildberries.ru/content/v1/tag/{id}"


async def a_patch_tag_change(tag_id: int, color: str, name: str) -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
        "color": color,
        "name": name,
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.patch(url=URL.format(id=tag_id), json=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(response.url)
                print(response.content_type)
                print(response.request_info)
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_req = {
        "color": "ECDAFF",
        "name": "Sale",
    }
    tag_id = 473766
    pprint.pp(asyncio.run(a_patch_tag_change(tag_id=tag_id, **sample_req)))
