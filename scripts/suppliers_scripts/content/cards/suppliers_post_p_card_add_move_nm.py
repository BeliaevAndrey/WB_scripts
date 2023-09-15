"""
Объединение / Разъединение НМ
https://openapi.wildberries.ru/#tag/Kontent-Zagruzka/paths/~1content~1v1~1cards~1moveNm/post

Метод позволяет объединять номенклатуры (nmID) под одним imtID и разъединять их.
Для объединения НМ необходимо отправить запрос со списком НМ с заполненным параметром targetIMT в
теле запроса. При этом все НМ объединятся под imtID указанном в targetIMT.

Чтобы отсоединить НМ от карточки, необходимо передать эту НМ без параметра targetIMT в теле запроса.
При этом для передаваемой НМ создается новый imtID.
Если в запросе передается несколько НМ, то все они автоматически объединятся под новым imtID.
Для НМ, не участвующих в запросе, никаких изменений не происходит.

ВАЖНО: Объединить можно только номенклатуры с одинаковыми предметами.
ВАЖНО: В одной КТ (под одним imtID) не может быть больше 30 номенклатур (nmID).


Request Body schema: application/json

1) requestMoveNmsImtConn
targetIMT(REQUIRED) -- integer -- Существующий у продавца imtID, под которым необходимо объединить НМ
nmIDs(REQUIRED) -- Array of integers -- nmID, которые необходимо объединить (max 30)

2) requestMoveNmsImtDisconn
nmIDs (REQUIRED) -- Array of integers -- nmID, которые необходимо разъединить (max 30)

Request samples
1)
{
  "targetIMT": 123,
  "nmIDs": [837459235, 828572090]
}

2)
{
  "nmIDs": [837459235, 828572090]
}

200
{
  "data": null,
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


async def a_supp_post_card_move_nm(data: dict) -> dict | tuple:
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
        "vendorCode": "6000000001",
        "cards": [
            {"characteristics": [
                    {"ТНВЭД": "4203100001"},
                    {"Ширина упаковки": 2},
                    {"Длина упаковки": 2},
                    {"Высота упаковки": 2},
                    {"Пол": ["Женский"]},
                    {"Цвет": "красный"},
                    {"Предмет": "Платья"},
                    {"Стилистика": ["casual"]},
                    {"Комплектация": ["Платье женское - 1шт"]},
                    {"Бренд": ["GlisH"]}
                ],
                "vendorCode": "6000000002",
                "sizes": [{"techSize": "38-39",
                           "wbSize": "38-39",
                           "price": 3000,
                           "skus": ["test333333331"]}
                          ]}
        ]
    }
    pprint.pp(asyncio.run(a_supp_post_card_move_nm(sample_req)))
