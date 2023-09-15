"""
Статистика/Методы статистики (Лимит по запросам: один запрос одного метода в минуту.)
Отчет о продажах по реализации
https://openapi.wildberries.ru/#tag/Statistika/paths/~1api~1v1~1supplier~1reportDetailByPeriod/get

Отчет о продажах по реализации.
В отчете доступны данные за последние 3 месяца.
В случае отсутствия данных за указанный период метод вернет null.
Технический перерыв в работе метода: каждый понедельник с 3:00 до 16:00.

dateFrom (REQUIRED) -- string <RFC3339> -- Дата и время последнего изменения по товару.
                                           Дата в формате RFC3339. Можно передать дату или
                                           дату со временем. Время можно указывать с точностью
                                           до секунд или миллисекунд.
                                           Литера Z в конце строки означает, что время
                                           передается в UTC-часовом поясе.
                                           При ее отсутствии время считается в часовом поясе
                                           Мск (UTC+3).
limit -- integer -- Default: 100000 Максимальное количество строк отчета,
                    возвращаемых методом. Не может быть более 100000.
dateTo (REQUIRED) -- string <date> -- Конечная дата отчета
rrdid -- integer -- Уникальный идентификатор строки отчета. Необходим для получения отчета частями.
                    Загрузку отчета нужно начинать с rrdid = 0 и при последующих вызовах API
                    передавать в запросе значение rrd_id из последней строки, полученной в
                    результате предыдущего вызова.
                    Таким образом для загрузки одного отчета может понадобиться вызывать
                    API до тех пор, пока количество возвращаемых строк не станет равным нулю.

200 -- Список реализованных позиций
401 -- ошибка авторизации

"""

from __future__ import annotations

import aiohttp
import asyncio
from time import sleep

from wb_secrets import token as __token

URL = "https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod"

count = 0


async def a_get_statistics_report(dateFrom: str,
                                  dateTo: str,
                                  flag: int = 0,
                                  limit: int = 100000,
                                  rrdid: int = 0,
                                  responses: list = None
                                  ):
    global count
    if responses is None:
        responses = []

    headers_dict = {
        "Authorization": __token,
    }

    params = {
        "dateFrom": dateFrom,
        "dateTo": dateTo,
        "limit": limit,
        "flag": flag,
        "rrdid": rrdid,

    }
    count += 1

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                if await response.text():
                    print(f'{response.status=}')
                    tmp = await response.json()
                    if tmp:
                        await asyncio.sleep(5)
                        responses.append(tmp)
                        report_id = tmp[-1].get("rrd_id")
                        return await a_get_statistics_report(dateFrom, dateTo, flag, limit,
                                                             report_id, responses,
                                                             )
                    else:
                        return responses
                else:
                    print(f'Finished, {response.status}')
                    return responses
            else:
                print(f'{response.status=}')
                return responses


if __name__ == '__main__':
    from datetime import datetime as _dt, timedelta as _dlt
    import pprint

    sample_req = {
        'dateFrom': (_dt.now() - _dlt(days=15)).isoformat(),
        'dateTo': (_dt.now() - _dlt(days=10)).isoformat()
    }
    pprint.pp(asyncio.run(a_get_statistics_report(**sample_req)))
