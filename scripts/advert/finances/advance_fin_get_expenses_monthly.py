"""
Получение месячных интервалов для истории затрат
https://openapi.wildberries.ru/#tag/Prodvizhenie-Finansy/paths/~1adv~1v1~1upd~1intervals/get

Метод позволяет получать информацию о бюджете кампании. new
Допускается максимум 240 запросов в минуту.

Responses
200
Response Schema: application/json
Array [string <time-date>]

400 -- "Некорректный идентификатор продавца"
401 -- ошибка авторизации
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/upd/intervals"


async def advance_fin_get_expenses_monthly():
    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint
    pprint.pp(asyncio.run(advance_fin_get_expenses_monthly()))
