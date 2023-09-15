"""
Получение истории пополнений счета
https://openapi.wildberries.ru/#tag/Prodvizhenie-Finansy/paths/~1adv~1v1~1upd~1intervals/get

Метод позволяет получать историю пополнений счёта.

date format: 2023-07-31

query Parameters
from -- string <date> -- Начало интервала
to -- string <date> -- Конец интервала. (Минимальный интервал 1 день, максимальный 31)

Responses
200
Response Schema: application/json
Array[
id -- integer -- Идентификатор платежа
date -- string <time-date> -- Дата платежа
sum --integer -- Сумма платежа
type -- integer -- Тип источника списания: 0 - balance; 1 - net; 3 - картой

statusId -- integer -- Статус: 0 - ошибка; 1 - обработано

cardStatus -- string -- Статус операции(при оплате картой): success - успех; fail - неуспех;
                                                            pending - в ожидании ответа;
                                                            unknown - неизвестно
]

400 -- "Некорректный идентификатор продавца"
401 -- ошибка авторизации
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/payments"


async def advance_fin_get_balance_refill_history(date_from, date_to):
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
            advance_get_balance_refill_history(sample_data[index].split('T')[0],
                                         sample_data[index - 1].split('T')[0])
        ))
