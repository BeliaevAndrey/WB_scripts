"""
Установка скидок
https://openapi.wildberries.ru/#tag/Promokody-i-skidki/paths/~1public~1api~1v1~1updateDiscounts/post

Установка скидок для номенклатур. Максимальное количество номенклатур на запрос - 1000.
Если, указав activateFrom больше текущей даты, Вы получаете ошибку вида
 {"errors": [ "Invalid activation date"], "error_code": 1},
значит, Ваш аккаунт переведен на систему Цены и скидки NEW, и эта опция более не доступна.
Отправьте запрос, указав настоящую дату.

Query Parameters
activateFrom    string  Дата активации скидки в формате
                        YYYY-MM-DD или YYYY-MM-DD HH:MM:SS.
                        Если не указывать, скидка начнет действовать сразу.

Request Body schema: application/json
 Array
discount    integer     Размер скидки
nm          integer     Артикул WB

Request samples
[{
    "discount": 15,
    "nm": 1234567
  }]

Response samples


400
{ "error": ["Invalid activation date"], "error_code": 1 }
{"error": ["No goods for process"], "error_code": 1}

{"errors":["incorrect data"]}

401
proxy: unauthorized
405
'See https://openapi.wb.ru'
"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/public/api/v1/updateDiscounts"


async def a_get_supp_set_discounts(discount: int, nm: int, activateFrom: str = ''):
    headers = {
        'Authorization': __token,
    }

    params = {
        "discount": discount,
        "nm": nm,
    }

    if activateFrom:
        params.update({'activateFrom': activateFrom})

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(params)
                print(response.url)
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_req = {
        "discount": 84,
        "nm": 163868337,
    }

    pprint.pp(asyncio.run(a_get_supp_set_discounts(**sample_req)))
