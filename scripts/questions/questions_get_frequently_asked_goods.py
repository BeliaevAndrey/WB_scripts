"""
Часто спрашиваемые товары
https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1questions~1products~1rating/get

Метод позволяет получить товары, про которые чаще всего спрашивают.

Query Parameters
size(REQUIRED) -- integer -- Количество запрашиваемых товаров (max. 100)

200
Response Schema: application/json
data -- object
    products -- Array of objects -- Массив структур товаров
        Array[
            nmId -- integer -- Артикул WB
            imtId -- integer -- Идентификатор карточки товара
            productName -- string -- Название товара
            brandName -- string -- Бренд товара
            questionsCount -- string -- Количество вопросов
            ]
error -- boolean -- Есть ли ошибка
errorText -- string -- Описание ошибки
additionalErrors -- Array of strings or null -- Дополнительные ошибки


401 -- authorization error
403
{ "data": null,
  "error": true,
  "errorText": "Ошибка авторизации",
  "additionalErrors": null}
"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://feedbacks-api.wildberries.ru/api/v1/questions/products/rating"
URL2 = "https://feedbacks-api.wb.ru/api/v1/questions/products/rating"


async def questions_get_frequently_asked_goods(size: int):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "size": size
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    pprint.pp(asyncio.run(questions_get_frequently_asked_goods(100)))
