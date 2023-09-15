"""
Список отзывов
https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks/get

Метод позволяет получить список отзывов по заданным параметрам с пагинацией и сортировкой.

Query Parameters
isAnswered(REQUIRED) -- boolean -- Обработанные отзывы (true) или необработанные отзывы(false)
nmId -- integer -- Артикул WB
take (REQUIRED )-- integer -- Количество отзывов (max. 5 000)
skip (REQUIRED) -- integer -- Количество отзывов для пропуска (max. 199990)
order -- string -- Сортировка отзывов по дате (dateAsc/dateDesc)
dateFrom -- integer -- Дата начала периода в формате Unix timestamp
dateTo -- integer -- Дата конца периода в формате Unix timestamp


200
Response samples:
{
  "data": {
    "countUnanswered": 1,
    "countArchive": 1,
    "feedbacks": [
      {
        "id": "n5um6IUBQOOSTxXoo0gV",
        "imtId": 4702466,
        "nmId": 5870243,
        "subjectId": 390,
        "userName": "userName",
        "text": "Great product. Thank you",
        "productValuation": 5,
        "createdDate": "2023-01-25T11:18:33Z",
        "updatedDate": "2023-01-26T11:09:54Z",
        "answer": null,
        "state": "none",
        "productDetails": {
          "imtId": 4702466,
          "nmId": 5870243,
          "productName": "Case for phone",
          "supplierArticle": "41058/transparent",
          "supplierName": "ГП Реклама и услуги",
          "brandName": "1000 Catalog",
          "size": "size"
        },
        "photoLinks": [
          {
            "fullSize": "feedbacks/470/4702466/2dc59933-00b5-4ba5-a11a-96312ef179f1_fs.jpg",
            "miniSize": "feedbacks/470/4702466/2dc59933-00b5-4ba5-a11a-96312ef179f1_ms.jpg"
          }
        ],
        "video": null,
        "wasViewed": true
      }
    ]
  },
  "error": false,
  "errorText": "",
  "additionalErrors": null
}

400
{   "data": null,
    "error": true,
    "errorText": "Something went wrong",
    "additionalErrors": null}
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

URL = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"
URL2 = "https://feedbacks-api.wb.ru/api/v1/feedbacks"


async def feedback_get_feedback_list(isAnswered: str,
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
        "isAnswered": "false",
        "take": 5000,
        "skip": 0,
    }

    pprint.pp(asyncio.run(feedback_get_feedback_list(**sample_data)))
