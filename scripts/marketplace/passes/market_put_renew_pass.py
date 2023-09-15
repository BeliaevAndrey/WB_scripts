"""
Обновить пропуск
https://openapi.wildberries.ru/#tag/Marketplace-Propuska/paths/~1api~1v3~1passes~1{passId}/put

Обновляет данные пропуска продавца.

path Parameters
passId (required) -- integer <int64> -- ID пропуска

Request Body schema: application/json
firstName (required) -- string non-empty -- Имя водителя
lastName (required) -- string non-empty -- Фамилия водителя
carModel (REQUIRED) -- string [ 1 .. 100 ] characters -- Марка машины
carNumber (REQUIRED) -- string [ 6 .. 9 ] characters -- Номер машины
officeId (REQUIRED) -- integer <int64> -- ID склада

204 -- Обновлено

400 -- Зарос содержит некорректные данные.
401 -- ошибка авторизации
403 -- доступ запрещен
404 -- ресурс не найден
429 -- превышен лимит запросов
500 -- ошибка сервера
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/passes/{passId}"


async def market_get_passes_list(passId: int, data: dict[str, str | int]):

    headers_dict = {
        "Authorization": __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.put(url=URL.format(passId=passId), json=data) as response:
            if response.status == 204:
                return await response.text()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint
    sample_data = {
            "firstName": "Александр",
            "lastName": "Петров",
            "carModel": "Lamborghini",
            "carNumber": "A456BC123",
            "officeId": 15
        }
    pprint.pp(asyncio.run(market_get_passes_list(9029381, sample_data)))
