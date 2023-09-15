"""
Создать пропуск
https://openapi.wildberries.ru/#tag/Marketplace-Propuska/paths/~1api~1v3~1passes/post

Создает пропуск продавца.
Пропуск действует 48 часов со времени создания. Метод ограничен одним вызовом в 10 минут.

Общая длина ФИО ограничена от 6 до 100 символов. В номере машины могут быть только буквы и цифры.

Request Body schema: application/json
firstName (required) -- string non-empty -- Имя водителя
lastName (required) -- string non-empty -- Фамилия водителя
carModel (REQUIRED) -- string [ 1 .. 100 ] characters -- Марка машины
carNumber (REQUIRED) -- string [ 6 .. 9 ] characters -- Номер машины
officeId (REQUIRED) -- integer <int64> -- ID склада

201 -- Created
Response Schema: application/json
id -- integer -- ID пропуска продавца

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

URL = "https://suppliers-api.wildberries.ru/api/v3/passes"


async def market_get_passes_list(data: dict[str, str | int]):

    headers_dict = {
        "Authorization": __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=data) as response:
            if response.status == 201:
                return await response.json()
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
    pprint.pp(asyncio.run(market_get_passes_list(sample_data)))
