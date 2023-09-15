"""
Статистика автоматической кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie-Statistika/paths/~1adv~1v1~1auto~1stat/get

Метод позволяет получать краткую статистику по автоматической кампании.
Допускается максимум 120 запросов в минуту.

Query Parameters
id(REQUIRED) -- integer -- Идентификатор кампании

Responses
200
Response Schema: application/json
views - integer -- Количество просмотров
clicks -- number -- Количество кликов
ctr -- number -- CTR (Click-Through Rate) — показатель кликабельности. Отношение числа
                                            кликов к количеству показов. Выражается в процентах.
cpc -- number -- CPC(от англ. cost per click — цена за клик) — это цена клика по продвигаемому товару.
spend -- integer -- Затраты, ₽.


400
{"error": "кампания не найдена"}
or
{"error": "доступно только для автоматических кампаний"}

401 -- ошибка авторизации
429 -- Превышен лимит запросов
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/auto/stat"


async def advance_stat_get_auto_camp_stat(comp_id: int):
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

    pprint.pp(asyncio.run(advance_stat_get_auto_camp_stat(sample_id)))
