"""
Список кампаний
https://openapi.wildberries.ru/#tag/Prodvizhenie/paths/~1adv~1v0~1adverts/get

Метод позволяет получить список кампании продавца.
Допускается максимум 300 запросов в минуту.

Query Parameters
status -- integer Enum: 4 7 9 11 -- Статус кампании
type -- integer Enum: 4 5 6 7 -- Тип кампании
limit -- integer -- Количество кампаний в ответе
offset -- integer -- Смещение относительно первой кампании
order -- string -- Enum: "create" "change" "id" -- Порядок:
    create (по времени создания кампании)
    change (по времени последнего изменения кампании)
    id (по идентификатору кампании)

direction -- string -- Enum: "desc" "asc" -- Направление:
    desc (от большего к меньшему)
    asc (от меньшего к большему)

Например: **/adv/v0/adverts?type=6&limit=5&offset=10&order=change&direction=asc**

Responses
200
Response Schema: application/json
Array [
advertId -- integer -- Идентификатор кампании
type -- integer -- Тип кампании:
    4 - кампания в каталоге
    5 - кампания в карточке товара
    6 - кампания в поиске
    7 - кампания в рекомендациях на главной странице
    8 - автоматическая кампания new
    9 - поиск + каталог new
status -- integer -- Статус кампании:
    4 - готова к запуску new
    7 - кампания завершена
    8 - отказался
    9 - идут показы
    11 - кампания на паузе -- dailyBudget -- string -- Сумма дневного бюджета
createTime -- string -- Время создания кампании
changeTime -- string -- Время последнего изменения кампании
startTime -- string -- Время последнего запуска кампании
endTime -- string -- Время завершения кампании (state 7)
]

400 -- "Некорректный идентификатор продавца"/"Некорректное значение параметра type"
401 -- ошибка авторизации
422 -- "Ошибка обработки параметров запроса"
"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/adverts"


async def advance_get_companies_list(data: list):
    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = [{"advertId": 456,
                    "type": 6,
                    "status": 11,
                    "dailyBudget": "string",
                    "createTime": "2022-03-09T10:50:21.831623+03:00",
                    "changeTime": "2022-12-22T18:24:19.808701+03:00",
                    "startTime": "2022-03-09T12:50:21.831623+03:00",
                    "endTime": "2022-11-09T14:40:21.831623+03:00"}]

    pprint.pp(asyncio.run(advance_get_companies_list(sample_data)))
