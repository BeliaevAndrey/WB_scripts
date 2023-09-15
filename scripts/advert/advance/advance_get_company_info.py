"""
Информация о кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie/paths/~1adv~1v0~1advert/get

Получение информации об одной кампании.
Важно: Чтобы у кампании со статусом 4 отображалась структура params необходимо после
создания кампании нажать кнопку "Применить изменения" в кабинете ВБ. Продвижение.
Допускается максимум 300 запросов в минуту.

Query Parameters

id(REQUIRED) -- integer -- Идентификатор кампании

Responses
200 -- ResponseInfoAdvert/ResponseInfoAdvertType8/ResponseInfoAdvertType9
204 -- Компания не найдена

400 -- "Некорректный идентификатор продавца"/"Некорректное значение параметра type"
401 -- ошибка авторизации
422 -- "Ошибка обработки параметров запроса"
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/advert"


async def advance_get_company_info(company_id: int):
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

    pprint.pp(asyncio.run(advance_get_company_info(7111417)))
