"""
Полная статистика кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie-Statistika/paths/~1adv~1v1~1fullstat/get

Метод позволяет получать расширенную статистку кампании, разделенную по дням,
номенклатурам и платформам (сайт, андроид, IOS).
Информация обновляется каждые два часа.
Допускается максимум 120 запросов в минуту.
Важно! Для кампаний в статусе 7 - Кампания завершена - параметры begin и end неприменимы.
Получить данные по таким кампаниям можно только сразу за всё время.


Query Parameters
id(REQUIRED) -- integer -- Идентификатор кампании
begin -- string -- Начало запрашиваемого периода. (Example: begin=2023-05-03)
end -- string -- Конец запрашиваемого периода. (Example: end=2023-06-19)


Responses
200
Response sample:
{
"advertId": 775675446,
"begin": "2023-07-03T00:00:00+03:00",
"end": "2023-07-12T00:00:00+03:00",
"days": [...],
"views": 3542,
"clicks": 134,
"frq": 1.11,
"unique_users": 3204,
"ctr": 3.78,
"cpc": 8.23,
"sum": 1102.52,
"atbs": 2,
"orders": 2,
"cr": 1.49,
"shks": 0,
"sum_price": 0,
"detailed": true,
"boosterStats": [...]
}

400
{"error": "кампания не найдена"}
or
{"error": "Некорректная дата начала"}
or
{"error": "Некорректная дата конца"}
or
{"error":"статистика в процессе получения"}

401 -- ошибка авторизации
429 -- Превышен лимит запросов
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/fullstat"


async def advance_stat_get_camp_full_stat(comp_id: int, begin: str = None, end: str = None):
    headers_dict = {
        'Authorization': __token
    }

    params = {
        "id": comp_id
    }

    if begin:
        params.update(begin=begin)
    if end:
        params.update(end=end)

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_id = 1
    sample_begin = "2023-05-03"
    sample_end = "2023-06-19"

    pprint.pp(asyncio.run(advance_stat_get_camp_full_stat(sample_id)))
