"""
Редактирование КТ
https://openapi.wildberries.ru/#tag/Kontent-Zagruzka/paths/~1content~1v1~1cards~1update/post

Метод позволяет отредактировать несколько карточек за раз.
Редактирование КТ происходит асинхронно, после отправки запрос становится в очередь на обработку.

ВАЖНО: Баркоды (skus) не подлежат удалению или замене. Попытка заменить существующий
баркод приведет к добавлению нового баркода к существующему.
Если запрос прошел успешно, а информация в карточке не обновилась, значит были допущены
ошибки и карточка попала в "Черновики" (метод cards/error/list) с описанием ошибок.
Необходимо исправить ошибки в запросе и отправить его повторно.

Для успешного обновления карточки рекомендуем Вам придерживаться следующего порядка действий:
1. Сначала существующую карточку необходимо запросить методом cards/filter.
2. Забираем из ответа массив data.
3. В этом массиве вносим необходимые изменения и отправляем его в cards/update

За раз можно отредактировать 1000 КТ по 5 НМ в каждой.

ВАЖНО: Изменение цен данным методом невозможно, используйте метод Загрузка цен, раздел документации Цены.

Request Body schema: application/json
[
 imtID -- integer -- Идентификатор карточки товара

 nmID -- (REQUIRED) -- integer Артикул WB

 object -- string -- Предмет

 objectID -- integer -- Идентификатор предмета

 vendorCode (REQUIRED) -- string -- Артикул продавца

 mediaFiles -- Array of strings -- Медиафайлы номенклатуры. Фото, URL которого
                                   заканчивается на 1.jpg является главным в карточке.

Array (REQUIRED) -- Array of objects -- Массив размеров для номенклатуры (для безразмерного товара
                                        все равно нужно передавать данный массив без параметров
                                        (wbSize и techSize), но с chrtID и баркодом)
[
    Array techSize -- string -- Размер товара (пример S, M, L, XL, 42, 42-43)

    chrtID (REQUIRED) -- integer -- Числовой идентификатор размера для данной номенклатуры Wildberries
                                    Обязателен к заполнению для существующих размеров. Для добавляемых
                                    размеров не указывается.

    wbSize -- string -- Российский размер товара

    skus (REQUIRED) -- Array of strings -- Массив баркодов, строковых идентификаторов размеров товара
                                           (их можно сгенерировать с помощью API, см. раздел "Контент / Просмотр")

    characteristics (REQUIRED) -- Array of objects -- Массив характеристик, индивидуальный для каждой категории
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

    sample_req = [
        {
            "imtID": 85792498,
            "nmID": 66964219,                   # REQUIRED
            "object": "Рубашки",
            "objectID": 184,
            "vendorCode": "6000000001",         # REQUIRED
            "mediaFiles": '',  # '["string"],
            "sizes": [{                         # REQUIRED
                "techSize": "40-41",
                "chrtID": 116108635,            # REQUIRED
                "wbSize": "40-41",
                "skus": ["1000000001"]          # REQUIRED
            }],
            "characteristics": [                # REQUIRED
                {"ТНВЭД": ["6403993600"]},
                {"Пол": ["Мужской"]},
                {"Цвет": ["зеленый"]},
                {"Предмет": ["Блузки"]}
            ]
        }
    ]

    pprint.pp(asyncio.run(a_supp_post_card_edit(sample_req)))

# Request sample
# [
#   {
#     "imtID": 85792498,
#     "nmID": 66964219,
#     "object": "Рубашки",
#     "objectID": 184,
#     "vendorCode": "6000000001",
#     "mediaFiles": [
#       "string"
#     ],
#     "sizes": [
#       {
#         "techSize": "40-41",
#         "chrtID": 116108635,
#         "wbSize": "40-41",
#         "skus": [
#           "1000000001"
#         ]
#       }
#     ],
#     "characteristics": [
#       {
#         "ТНВЭД": [
#           "6403993600"
#         ]
#       },
#       {
#         "Пол": [
#           "Мужской"
#         ]
#       },
#       {
#         "Цвет": [
#           "зеленый"
#         ]
#       },
#       {
#         "Предмет": [
#           "Блузки"
#         ]
#       }
#     ]
#   }
# ]
