"""
Запуск кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie-Aktivnost-kampanii/paths/~1adv~1v0~1start/get

Метод позволяет запускать кампании находящиеся в статусах
4 - готова к запуску или 11 - кампания на паузе.
Для запуска кампании со статусом 11 необходимо наличие у неё активных ставок.

Чтобы запустить кампанию со статусом 4 необходимо выполнить два условия
(поочередность действий значения не имеет):
1. После создания кампании в кабинете ВБ. Продвижение
   необходимо нажать кнопку "Применить изменения".
2. Установить бюджет.

Допускается максимум 300 запросов в минуту.

Query Parameters
id (REQUIRED) -- integer -- Идентификатор кампании

Responses
200 -- Статус изменен
400 -- "Некорректный идентификатор РК"/"Некорректный идентификатор продавца"
401 -- ошибка авторизации
422 -- "Статус кампании не изменен"
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/start"


async def advance_activity_get_start_company(company_id):
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

    sample_data = 1234

    pprint.pp(asyncio.run(advance_activity_get_start_company(sample_data)))
