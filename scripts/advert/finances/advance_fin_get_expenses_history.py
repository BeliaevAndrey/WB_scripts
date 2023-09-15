"""
Получение истории затрат
https://openapi.wildberries.ru/#tag/Prodvizhenie-Finansy/paths/~1adv~1v1~1upd~1intervals/get

Метод позволяет получать историю затрат. new

query Parameters
from (REQUIRED) -- string <date> -- Начало интервала
to (REQUIRED) -- string <date>  -- Конец интервала. (Минимальный интервал 1 день, максимальный 31)

Responses
200
Response Schema: application/json
Array[
updNum -- integer -- Номер выставленного документа (при наличии)
updTime -- string <time-date> -- Время списания
updSum -- integer -- Выставленная сумма
advertId -- integer -- Идентификатор кампании
campName -- string -- Название кампании
advertType -- integer -- Тип кампании
paymentType -- string -- Источник списания: Баланс, Бонусы, Счет
advertStatus --integer -- Статус кампании: 4 - готова к запуску new ;
                                           7 - завершена; 8 - отказался;
                                           9 - активна; 11 - приостановлена
]

400 -- "Некорректный идентификатор продавца"
401 -- ошибка авторизации
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/upd"


async def advance_fin_get_expenses_history(date_from, date_to):
    headers_dict = {
        'Authorization': __token
    }

    params = {
        "from": date_from,
        "to": date_to
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint
    from advance_get_expenses_monthly import advance_get_expenses_monthly

    # sample_data = ['2023-09-01T00:00:00Z',
    #                '2023-08-01T00:00:00Z',
    #                '2023-07-01T00:00:00Z',
    #                '2023-06-01T00:00:00Z']

    sample_data = asyncio.run(advance_fin_get_expenses_monthly())

    for index in range(1, len(sample_data)):
        print(f'\n{sample_data[index].split("T")[0]:=>20} - {sample_data[index - 1].split("T")[0]:=<20}')
        pprint.pp(asyncio.run(
            advance_get_expenses_history(sample_data[index].split('T')[0],
                                         sample_data[index - 1].split('T')[0])
        ))
