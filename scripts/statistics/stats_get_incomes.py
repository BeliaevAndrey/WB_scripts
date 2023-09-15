"""
Статистика/Методы статистики. (Лимит по запросам: один запрос одного метода в минуту.)
Поставки.
https://openapi.wildberries.ru/#tag/Statistika/paths/~1api~1v1~1supplier~1incomes/get

Если Вы получили ошибку со статус-кодом 408 и текстом (api-new)
 request timeout подождите некоторое время и повторите запрос.

Query Parameters

dateFrom
required

string <RFC3339>

Дата и время последнего изменения по товару.
Для получения полного остатка следует указывать
максимально раннее значение.
Например, 2019-06-20
Дата в формате RFC3339. Можно передать дату или дату
со временем. Время можно указывать с точностью до секунд
или миллисекунд.
Литера Z в конце строки означает, что время передается в
UTC-часовом поясе.
При ее отсутствии время считается в часовом поясе Мск (UTC+3).


200
[{"incomeId": 12345,
    "number": "",
    "date": "2022-05-08T00:00:54",
    "lastChangeDate": "2022-05-08T00:44:15.5",
    "supplierArticle": "ABCDEF",
    "techSize": "0",
    "barcode": "2000328074123",
    "quantity": 3,
    "totalPrice": 0,
    "dateClose": "2022-05-08T00:00:00",
    "warehouseName": "Подольск",
    "nmId": 1234567,
    "status": "Принято"}]

401
proxy: unauthorized

408 --  Тайм-аут запроса
{
  "errors": [
    "(api-new) request timeout"
  ]
}
"""

import aiohttp
import asyncio

from wb_secrets import token as __token

URL = "https://statistics-api.wildberries.ru/api/v1/supplier/incomes"


async def a_get_statistics_incomes(dateFrom: str) -> [dict, tuple]:
    headers_dict = {
        "Authorization": __token,
    }

    params = {
        "dateFrom": dateFrom,
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    from datetime import datetime as _dt, timedelta as _dlt
    import pprint

    sample_req = {
        'dateFrom': (_dt.now() - _dlt(days=15)).isoformat()
    }
    pprint.pp(asyncio.run(a_get_statistics_incomes(**sample_req)))
