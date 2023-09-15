"""
Генерация баркодов
https://openapi.wildberries.ru/#tag/Kontent-Zagruzka/paths/~1content~1v1~1barcodes/post

Метод позволяет сгенерировать массив уникальных баркодов для создания размера НМ в КТ.

Request Body schema: application/json
count -- integer -- Кол-во баркодов которые надо сгенерировать,
                    максимальное доступное количество баркодов для генерации - 5000

Request samples
{
  "count": 1
}

Response samples
200
{
  "data": [
    "5032781145187"
  ],
  "error": false,
  "errorText": "",
  "additionalErrors": ""
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

URL = "https://suppliers-api.wildberries.ru/content/v1/cards/update"


async def a_supp_post_card_barcode_generate(count: int) -> dict | tuple:
    headers_dict = {
        'Authorization': __token,
    }

    params = {
        "count": count
    }
    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=params) as request:
            if request.status == 200:
                return await request.json()
            else:
                return request.status, await request.text()


if __name__ == '__main__':
    import pprint

    sample_req = {
        "count": 1
    }
    pprint.pp(asyncio.run(a_supp_post_card_barcode_generate(**sample_req)))
