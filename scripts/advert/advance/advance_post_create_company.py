"""
Создание кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie/paths/~1adv~1v1~1save-ad/post

Метод позволяет создавать кампании. new
Важно: На данный момент создавать можно только автоматические кампании.
Возможность создания остальных типов кампаний будет реализована позднее.

Request Body schema: application/json
type -- integer -- Тип создаваемой кампании: 8 - автоматическая кампания
name -- string -- Название кампании (max. 128 символов)
subjectId -- integer -- ID предмета, для которого создается кампания.
                        Существующие у продавца идентификаторы можно получить
                        методом из раздела "Контент / Просмотр" - "Список НМ",
                        поле ответа - objectID.
sum -- integer -- Сумма пополнения
btype -- integer -- Tип списания. 0 - balance; 1 - net; 3 - bonus


Responses
200
Response Schema: application/json
string -- ID созданной кампании

400 -- неверная форма запроса
401 -- ошибка авторизации
422 -- Ошибка обработки
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/save-ad"


async def advance_post_create_company(data: dict):
    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {"type": 8,
                   "name": "Парашюты",
                   "subjectId": 270,
                   "sum": 500,
                   "btype": 1}

    pprint.pp(asyncio.run(advance_post_create_company(sample_data)))
