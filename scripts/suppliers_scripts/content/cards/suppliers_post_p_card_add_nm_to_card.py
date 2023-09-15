"""
Добавление НМ к КТ
https://openapi.wildberries.ru/#tag/Kontent-Zagruzka/paths/~1content~1v1~1cards~1upload~1add/post

Метод позволяет добавить к карточке товара новую номенклатуру.
Добавление НМ к КТ происходит асинхронно, после отправки запрос становится в очередь на обработку.

ВАЖНО: Если после успешной отправки запроса номенклатура не создалась, то необходимо проверить
раздел "Список несозданных НМ с ошибками". Для того чтобы убрать НМ из ошибочных, необходимо
повторно сделать запрос с исправленными ошибками.

Request Body schema: application/json

vendorCode -- string -- Артикул продавца
cards -- Array of objects -- Массив НМ которые хотим добавить к КТ
[
vendorCode -- string -- Артикул продавца

characteristics -- Array of objects -- Массив характеристик, индивидуальный для каждой категории

sizes -- Array of objects
[
techSize -- string -- Размер товара (пример S, M, L, XL, 42, 42-43)
wbSize -- string -- Российский размер товара
price -- integer -- Цена (указывается в рублях)
skus -- Array of strings -- Массив баркодов, строковых идентификаторов размеров товара (их можно сгенерировать с помощью API, см. Viewer)
]
]

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


async def a_supp_post_card_add_nm_to_card(data: dict) -> dict | tuple:
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
    pprint.pp(asyncio.run(a_supp_post_card_add_nm_to_card(sample_req)))

# Request sample
# {
#   "vendorCode": "6000000001",
#   "cards": [
#     {
#       "characteristics": [
#         {
#           "ТНВЭД": "4203100001"
#         },
#         {
#           "Ширина упаковки": 2
#         },
#         {
#           "Длина упаковки": 2
#         },
#         {
#           "Высота упаковки": 2
#         },
#         {
#           "Пол": [
#             "Женский"
#           ]
#         },
#         {
#           "Цвет": "красный"
#         },
#         {
#           "Предмет": "Платья"
#         },
#         {
#           "Стилистика": [
#             "casual"
#           ]
#         },
#         {
#           "Комплектация": [
#             "Платье женское - 1шт"
#           ]
#         },
#         {
#           "Бренд": [
#             "GlisH"
#           ]
#         }
#       ],
#       "vendorCode": "6000000002",
#       "sizes": [
#         {
#           "techSize": "38-39",
#           "wbSize": "38-39",
#           "price": 3000,
#           "skus": [
#             "test333333331"
#           ]
#         }
#       ]
#     }
#   ]
# }
