"""
Сброс скидок для номенклатур
https://openapi.wildberries.ru/#tag/Promokody-i-skidki/paths/~1public~1api~1v1~1revokeDiscounts/post

Установка скидок для номенклатур. Максимальное количество номенклатур на запрос - 1000.
Если, указав activateFrom больше текущей даты, Вы получаете ошибку вида
 {"errors": [ "Invalid activation date"], "error_code": 1},
значит, Ваш аккаунт переведен на систему Цены и скидки NEW, и эта опция более не доступна.
Отправьте запрос, указав настоящую дату.

Query Parameters

Request Body schema: application/json

Array [integer] Перечень номенклатур к отмене скидок

Request samples
[12345678, 81234567]

Response samples
400
'{"errors":["incorrect data"]}\n'

401
proxy: unauthorized
"""

import aiohttp
import asyncio
import json

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/public/api/v1/revokeDiscounts"


async def a_get_supp_drop_discounts(discounts: list[int]):
    headers = {
        'Authorization': __token,
    }

    params = {
        discounts
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    pprint.pp(
        asyncio.run(
            a_get_supp_drop_discounts(
                [
                    12345678,
                    81234567
                ]
            )
        )
    )
