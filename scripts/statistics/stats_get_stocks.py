"""
Статистика/Методы статистики (Лимит по запросам: один запрос одного метода в минуту.)
Склад
https://openapi.wildberries.ru/#tag/Statistika/paths/~1api~1v1~1supplier~1stocks/get

Остатки товаров на складах WB. Данные обновляются раз в 30 минут.
Сервис статистики не хранит историю остатков товаров, поэтому
получить данные о них можно только в режиме "на текущий момент".
Если Вы получили ошибку со статус-кодом 408 и текстом (api-new)
request timeout подождите некоторое время и повторите запрос.

Query Parameters
dateFrom (REQUIRED) -- string <RFC3339>

Response Samples
[{   "lastChangeDate": "2023-07-05T11:13:35",
     "warehouseName": "Краснодар",
     "supplierArticle": "443284",
     "nmId": 1439871458,
     "barcode": "2037401340280",
     "quantity": 33,
     "inWayToClient": 1,
     "inWayFromClient": 0,
     "quantityFull": 34,
     "category": "Посуда и инвентарь",
     "subject": "Формы для запекания",
     "brand": "X",
     "techSize": "0",
     "Price": 185,
     "Discount": 0,
     "isSupply": true,
     "isRealization": false,
     "SCCode": "Tech"}]

401
proxy: unauthorized

408
{
  "errors": ["(api-new) request timeout"]
}

"""

import aiohttp
import asyncio

from wb_secrets import token as __token

URL = "https://statistics-api.wildberries.ru/api/v1/supplier/stocks"


async def a_get_statistics_stocks(dateFrom: str) -> [dict, tuple]:
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
    pprint.pp(asyncio.run(a_get_statistics_stocks(**sample_req)))
