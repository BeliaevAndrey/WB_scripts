"""
Список вопросов
https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1questions/get

Метод позволяет получить товары, про которые чаще всего спрашивают.

Query Parameters
isAnswered (REQUIRED) -- boolean -- Отвеченные вопросы (true) или неотвеченные вопросы(false)
nmId -- integer -- Артикул WB
take (REQUIRED )-- integer -- Количество запрашиваемых вопросов (максимально допустимое значение для параметра - 10 000, при этом сумма значений параметров take и skip не должна превышать 10 000)
skip (REQUIRED) -- integer -- Количество вопросов для пропуска (максимально допустимое значение для параметра - 10 000, при этом сумма значений параметров take и skip не должна превышать 10 000)
order -- string -- Сортировка вопросов по дате (dateAsc/dateDesc)
dateFrom -- integer -- Дата начала периода в формате Unix timestamp
dateTo -- integer -- Дата конца периода в формате Unix timestamp


200
Response samples:
{
  "data": {
    "countUnanswered": 24,
    "countArchive": 508,
    "questions": [
      {
        "id": "2ncBtX4B9I0UHoornoqG",
        "text": "Текст вопроса",
        "createdDate": "2022-02-01T11:18:08.769513469Z",
        "state": "suppliersPortalSynch",
        "answer": null,
        "productDetails": {
          "imtId": 11157265,
          "nmId": 14917842,
          "productName": "Кофе",
          "supplierArticle": "123401",
          "supplierName": " ГП Реклама и услуги",
          "brandName": "Nescofe"
        },
        "wasViewed": false,
        "isOverdue": true
      }
    ]
  },
  "error": false,
  "errorText": "",
  "additionalErrors": null
}

400
{

    "data": null,
    "error": true,
    "errorText": "Something went wrong",
    "additionalErrors": null

}
401 -- authorization error
403
{ "data": null,
  "error": true,
  "errorText": "Ошибка авторизации",
  "additionalErrors": null}
"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://feedbacks-api.wildberries.ru/api/v1/questions"
URL2 = "https://feedbacks-api.wb.ru/api/v1/questions"


async def questions_get_questions_list(isAnswered: str,
                                       take: int,
                                       skip: int,
                                       nmId: int = None,
                                       order: str = None,
                                       dateFrom: int = None,
                                       dateTo: int = None,
                                       ):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "isAnswered": isAnswered,
        "take": take,
        "skip": skip,
    }
    if nmId:
        params.update(nmId=nmId)
    if order:
        params.update(order=order)
    if dateFrom:
        params.update(dateFrom=dateFrom)
    if dateTo:
        params.update(dateTo=dateTo)

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "isAnswered": "True",
        "take": 1000,
        "skip": 1000,
    }

    pprint.pp(asyncio.run(questions_get_questions_list(**sample_data)))
