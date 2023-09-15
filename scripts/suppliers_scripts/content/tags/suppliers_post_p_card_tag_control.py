"""
Управление тегами в КТ
https://openapi.wildberries.ru/#tag/Kontent-Tegi/paths/~1content~1v1~1tag~1nomenclature~1link/post
Метод позволяет добавить теги к КТ и снять их с КТ.
При снятии тега с КТ сам тег не удаляется.
К карточке можно добавить 8 тегов.

Request Body schema: application/json
nmID        integer Артикул WB
tagsIDs     Array of integers   Массив числовых идентификаторов тегов.
                                Чтобы снять теги с КТ, необходимо передать
                                пустой массив.
                                Чтобы добавить теги к уже имеющимся в КТ,
                                необходимо в запросе передать новые теги и теги,
                                которые уже есть в КТ.

Request samples
{
  "nmID": 179891389,
  "tagsIDs": [123456]
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
    "errorText": "Неправильный запрос",
    "additionalErrors":
    {
        "description": "Указаны несуществующие теги"
    }
}

401 "proxy: unauthorized"

403
{ "data": null,
  "error": true,
  "errorText": "Доступ запрещен",
  "additionalErrors": "Доступ запрещен"
}

500
{
  "data": null,
  "error": true,
  "errorText": "Внутренняя ошибка.",
  "additionalErrors": null
}
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/content/v1/tag/nomenclature/link"


async def a_post_tag_control(nmID: int, tagsIDs: list[int]) -> tuple | dict:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
        "nmID": nmID,
        "tagsIDs": tagsIDs,
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
        "nmID": 179891389,
        "tagsIDs": [123456]
    }

    pprint.pp(asyncio.run(a_post_tag_control(**sample_req)))
