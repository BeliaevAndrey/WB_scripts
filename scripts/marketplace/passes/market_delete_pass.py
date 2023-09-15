"""
Удалить пропуск
https://openapi.wildberries.ru/#tag/Marketplace-Propuska/paths/~1api~1v3~1passes~1{passId}/delete

Удаляет пропуск продавца.

path Parameters
passId (required) -- integer <int64> -- ID пропуска

204 -- Удалено

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


async def market_get_passes_list(passId: int):

    headers_dict = {
        "Authorization": __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.delete(url=URL.format(passId=passId)) as response:
            if response.status == 204:
                return await response.text()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    pprint.pp(asyncio.run(market_get_passes_list(9029381)))
