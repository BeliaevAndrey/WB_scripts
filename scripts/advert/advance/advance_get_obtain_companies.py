"""
Получение кампаний
https://openapi.wildberries.ru/#tag/Prodvizhenie/paths/~1adv~1v0~1count/get

Получение количества кампаний поставщика.
Допускается максимум 300 запросов в минуту.

Responses

Response Schema: application/json
all -- integer -- Общее количество кампаний всех статусов и типов
adverts -- Array of objects -- Массив кампаний
[
type -- integer -- Тип кампании:
    4 - кампания в каталоге
    5 - кампания в карточке товара
    6 - кампания в поиске
    7 - кампания в рекомендациях на главной странице
    8 - автоматическая кампания new
    9 - поиск + каталог new
status -- integer -- Статус кампании:
    4 - готова к запуску new
    7 - Кампания завершена
    8 - отказался
    9 - идут показы
    11 - Кампания на паузе
count -- integer -- Количество кампаний
]

400 -- Некорректный идентификатор продавца
401 -- ошибка авторизации
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/count"


async def advance_get_obtain_companies():

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

    pprint.pp(asyncio.run(advance_get_obtain_companies()))
