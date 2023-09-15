"""
Получить список пропусков
https://openapi.wildberries.ru/#tag/Marketplace-Propuska/paths/~1api~1v3~1passes/get
Возвращает список всех пропусков продавца.


200 -- список пропусков продавца
Response Schema: application/json
Array
[
firstName -- string -- Имя водителя
dateEnd -- string -- Дата окончания действия пропуска
lastName -- string -- Фамилия водителя
carModel -- string -- Марка машины
carNumber -- string -- Номер машины
officeName -- string -- Название склада
officeAddress -- string -- Адрес склада
officeId -- integer <int64> -- ID склада
id -- integer <int64> -- ID пропуска
]

401 -- ошибка авторизации
403 -- доступ запрещен
429 -- превышен лимит запросов
500 -- ошибка сервера
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/passes"


async def market_get_passes_list():

    headers_dict = {
        "Authorization": __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    pprint.pp(asyncio.run(market_get_passes_list()))
