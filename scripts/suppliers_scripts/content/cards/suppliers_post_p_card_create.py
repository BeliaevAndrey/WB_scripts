"""
Создание КТ
https://openapi.wildberries.ru/#tag/Kontent-Zagruzka/paths/~1content~1v1~1cards~1upload/post

Создание карточки товара происходит асинхронно, при отправке запроса на создание
КТ ваш запрос становится в очередь на создание КТ.
ПРИМЕЧАНИЕ: Карточка товара считается созданной, если успешно создалась хотя бы одна НМ.
ВАЖНО: Если во время обработки запроса в очереди выявляются ошибки, то НМ считается ошибочной.
Если запрос на создание прошел успешно, а карточка не создалась, то необходимо в первую очередь
проверить наличие карточки в методе cards/error/list. Если карточка попала в ответ к этому методу,
то необходимо исправить описанные ошибки в запросе на создание карточки и отправить его повторно.
За раз можно создать 1000 КТ по 5 НМ в каждой.
Если Вам требуется больше 5 НМ в КТ, то после создания карточки Вы можете добавить их методом
"Добавление НМ к КТ".

Request Body schema: application/json

[
    [
        characteristics     Array of objects    Массив характеристик, индивидуальный для каждой категории
        vendorCode          string              Артикул продавца
        sizes               Array of objects    Массив размеров для номенклатуры (для безразмерного товара
                                                все равно нужно передавать данный массив без параметров
                                                (wbSize и techSize), но с ценой и баркодом)
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

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/content/v1/cards/upload"


async def a_supp_post_card_edit(data: list) -> dict | tuple:
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

    sample_req = [[{
        "characteristics": [
            {"ТНВЭД": "4203100001"},
            {"Ширина упаковки": 2},
            {"Длина упаковки": 2},
            {"Высота упаковки": 2},
            {"Пол": ["Женский"]},
            {"Цвет": "красный"},
            {"Предмет": "Платья"},
            {"Стилистика": ["casual"]},
            {"Комплектация": ["Платье женское - 1шт"]},
            {"Бренд": ["GlisH"]}],
        "vendorCode": "ttteeessstt-1",
        "sizes": [{
            "techSize": "38-39",
            "wbSize": "38-39",
            "price": 3000,
            "skus": ["test333333331"]
        }]
    }]]

    pprint.pp(asyncio.run(a_supp_post_card_edit(sample_req)))

# Request sample
# [
#   [
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
#       "vendorCode": "ttteeessstt-1",
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
# ]
