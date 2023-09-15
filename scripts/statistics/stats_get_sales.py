"""
Статистика/Методы статистики (Лимит по запросам: один запрос одного метода в минуту.)
Заказы
https://openapi.wildberries.ru/#tag/Statistika/paths/~1api~1v1~1supplier~1orders/get

Заказы.
Важно: гарантируется хранение данных по заказам не более 90 дней от даты заказа.
Данные обновляются раз в 30 минут. Точное время обновления информации в сервисе
можно увидеть в поле lastChangeDate.
Для идентификации товаров из одного заказа, а также продаж по ним, следует
использовать поле gNumber (строки с одинаковым значением этого поля относятся к
одному заказу) и номер уникальной позиции в заказе odid (rid).

Если Вы получили ошибку со статус-кодом 408 и текстом (api-new) request timeout
 подождите некоторое время и повторите запрос.

Query Parameters
dateFrom (REQUIRED) -- string <RFC3339> -- Дата и время последнего изменения по товару.
                                           Дата в формате RFC3339. Можно передать дату или дату со временем.
                                           Время можно указывать с точностью до секунд или миллисекунд.
                                           Литера Z в конце строки означает, что время передается в UTC-часовом поясе.
                                           При ее отсутствии время считается в часовом поясе Мск (UTC+3).

flag    integer Default: 0
    * flag=0 (или не указан в строке запроса),
    при вызове API возвращаются данные, у которых значение поля
    lastChangeDate (дата время обновления информации в сервисе)
    больше или равно переданному значению параметра dateFrom.
    При этом количество возвращенных строк данных варьируется в
    интервале от 0 до примерно 100 000.
    * flag=1, то будет выгружена информация обо всех заказах или
    продажах с датой, равной переданному параметру dateFrom
    (в данном случае время в дате значения не имеет).
    При этом количество возвращенных строк данных будет равно
    количеству всех заказов или продаж, сделанных в указанную дату,
     переданную в параметре dateFrom.

Response Samples
200
[{  "date": "2022-03-02T14:34:05",
    "lastChangeDate": "2022-03-02T19:30:16",
    "supplierArticle": "12345",
    "techSize": "0",
    "barcode": "9990016520011",
    "totalPrice": 120.56,
    "discountPercent": 0,
    "warehouseName": "Екатеринбург",
    "oblast": "Московская",
    "incomeID": 123456,
    "odid": 12345678,
    "nmId": 12345678,
    "subject": "Респираторы",
    "category": "Спецодежда и СИЗы",
    "brand": "wildberries",
    "isCancel": false,
    "cancel_dt": "0001-01-01T00:00:00",
    "gNumber": "12345678",
    "sticker": "",
    "orderType": "Клиентский"
 }]

400
{
  "errors": ["can't parse dateFrom"]
}

401
proxy: unauthorized
or
proxy: invalid token
or
Используемый токен не применим к данным методам.
Error ae394f96-e258-432d-af13-a53a3d31f8b0: request rejected, unathorized: token scope not allowed for this API route
or
Токен удален
proxy: not found

408
{
  "errors": ["(api-new) request timeout"]
}
"""

import aiohttp
import asyncio

from wb_secrets import token as __token

URL = "https://statistics-api.wildberries.ru/api/v1/supplier/sales"


async def a_get_statistics_sales(dateFrom: str,
                                 flag: int = 0) -> [dict, tuple]:

    headers_dict = {
        "Authorization": __token,
    }

    params = {
        "dateFrom": dateFrom,
        "flag": flag,

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
        'dateFrom': (_dt.now() - _dlt(days=15)).isoformat(),
        'flag': 1
    }
    pprint.pp(asyncio.run(a_get_statistics_sales(**sample_req)))
