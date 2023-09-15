"""
Бюджет кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie-Finansy/paths/~1adv~1v1~1budget/get

Метод позволяет получать информацию о бюджете кампании. new
Допускается максимум 240 запросов в минуту.

query Parameters
id (REQUIRED) -- integer -- Идентификатор кампании

Responses
200
Response Schema: application/json
cash -- integer -- Поле не используется. Значение всегда 0.
netting -- integer -- Поле не используется. Значение всегда 0.
total -- integer -- Бюджет кампании, ₽

400 -- "Некорректный идентификатор продавца"
401 -- ошибка авторизации
429 -- превышен лимит запросов
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/budget"


async def advance_fin_get_budget(company_id: int):
    headers_dict = {
        'Authorization': __token
    }

    params = {
        "id": company_id
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint
    sample_data = 1
    pprint.pp(asyncio.run(advance_fin_get_budget(sample_data)))
