"""
Словарь значений параметра menuId
https://openapi.wildberries.ru/#tag/Prodvizhenie-Slovari/paths/~1adv~1v0~1params~1menu/get

Метод позволяет получить список значений параметра menuId.
Допускается максимум 300 запросов в минуту.

Query Parameters

id -- integer -- Идентификатор предметной группы, для которой создана кампания
                (для кампаний в поиске и рекомендациях).
                Принимает значение параметра menuId из кампании.
                При пустом параметре вернётся весь список существующих значений.

Responses
200
Response Schema: application/json
Array [
id -- integer -- Значение для параметра menuId
name -- string -- Название меню, где размещается кампания
]

400 -- "Некорректный идентификатор продавца"
401 -- ошибка авторизации

"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/params/menu"


async def advance_get_dict_of_subjectId(menuId: int):
    headers_dict = {
        'Authorization': __token
    }

    params = {
        "id": menuId
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint
    sample_data = 8967
    pprint.pp(asyncio.run(advance_get_dict_of_subjectId(sample_data)))
