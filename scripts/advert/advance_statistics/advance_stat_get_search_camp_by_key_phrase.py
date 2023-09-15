"""
Статистика поисковой кампании по ключевым фразам
https://openapi.wildberries.ru/#tag/Prodvizhenie-Statistika/paths/~1adv~1v1~1stat~1words/get

Метод позволяет получать статистику поисковой кампании по ключевым фразам.
Информация обновляется примерно каждые полчаса.
Допускается максимум 240 запросов в минуту.

Query Parameters
id(REQUIRED) -- integer -- Идентификатор кампании

Responses
200
Response Schema: application/json
words -- json object -- Блок информации по ключевым фразам
stat -- Array of objects -- Массив информации по статистике.
Первый элемент массива с keyword: "Всего по кампании" содержит суммарную информацию по всем ключевым фразам.
Каждый следующий элемент массива содержит информацию по отдельной ключевой фразе.
Отображается 60 ключевых фраз с наибольшим количеством просмотров.


400 -- "Некорректный идентификатор продавца"/"Некорректное значение параметра type"
401 -- ошибка авторизации
429 -- Превышен лимит запросов
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/stat/words"


async def advance_stat_get_search_camp_by_key_phrase(comp_id: int):
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

    pprint.pp(asyncio.run(advance_stat_get_search_camp_by_key_phrase(sample_id)))
