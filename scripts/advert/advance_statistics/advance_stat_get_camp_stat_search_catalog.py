"""
Статистика кампаний Поиск + Каталог
https://openapi.wildberries.ru/#tag/Prodvizhenie-Statistika/paths/~1adv~1v1~1seacat~1stat/get

Метод позволяет получать статистику по кампаниям Поиск + Каталог.
Допускается максимум 60 запросов в минуту.

Query Parameters
id(REQUIRED) -- integer -- Идентификатор кампании

Responses
200
Response Schema: application/json
totalViews -- integer -- Суммарное количество просмотров
totalClicks -- integer -- Суммарное количество кликов
totalOrders -- integer -- Суммарное количество заказов
totalSum -- integer -- Суммарные затраты, ₽.
dates -- Array of objects -- Блок статистики

400
{"error": "кампания не найдена"}
or
{"error": "доступно только для активных кампаний"}

401 -- ошибка авторизации
429 -- Превышен лимит запросов
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/seacat/stat"


async def advance_stat_get_camp_stat_search_catalog(comp_id: int):
    headers_dict = {
        'Authorization': __token
    }

    params = {
        "id": comp_id
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_id = 1

    pprint.pp(asyncio.run(advance_stat_get_camp_stat_search_catalog(sample_id)))
