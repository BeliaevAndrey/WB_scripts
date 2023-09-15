"""
Словарь значений параметра subjectId
https://openapi.wildberries.ru/#tag/Prodvizhenie-Slovari/paths/~1adv~1v0~1params~1subject/get

Метод позволяет получить список значений параметра subjectId.
Допускается максимум 300 запросов в минуту.

Query Parameters

id -- integer -- Идентификатор предметной группы, для которой создана кампания
                (для кампаний в поиске и рекомендациях).
                Принимает значение параметра subjectId из кампании.
                При пустом параметре вернётся весь список существующих значений.

Responses
200
Response Schema: application/json
Array [
id -- integer -- Значение для параметра subjectId
name -- string -- Название предметной группы, для которой создана кампания
]

400 -- "Некорректный идентификатор продавца"
401 -- ошибка авторизации

"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/params/subject"


async def advance_get_dict_of_subjectId(subjectId: int):
    headers_dict = {
        'Authorization': __token
    }

    params = {
        "id": subjectId
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint
    sample_data = 699
    pprint.pp(asyncio.run(advance_get_dict_of_subjectId(sample_data)))
