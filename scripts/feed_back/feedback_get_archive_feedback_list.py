"""
Список архивных отзывов
https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1archive/get

Метод позволяет получить список архивных отзывов.
Отзыв становится архивным если на него предоставлен
ответ или ответ не предоставлен в течение 30 дней со дня его публикации.

Query Parameters
nmId -- integer Example: nmId=14917842 -- Артикул WB
take (REQUIRED) -- integer Example: take=1 -- Количество отзывов (max. 5 000)
skip (REQUIRED) -- integer Example: skip=0 -- Количество отзывов для пропуска
order -- string -- Сортировка отзывов по дате (dateAsc/dateDesc)

200
Response samples:
{
  "data": {
    "productMaxRating": {
      "nmId": 14917842,
      "imtId": 11157265,
      "subjectId": 5135,
      "valuationsSum": 1260,
      "feedbacksCount": 252,
      "valuation": 5,
      "productName": "Кофе",
      "supplierArticle": "123401",
      "brandName": "Nescafe"
    },
    "productMinRating": {
      "nmId": 14917846,
      "imtId": 11157269,
      "subjectId": 5134,
      "valuationsSum": 4,
      "feedbacksCount": 2,
      "valuation": 2,
      "productName": "Кофе",
      "supplierArticle": "425501",
      "brandName": "Nescafe"
    }
  },
  "error": false,
  "errorText": "",
  "additionalErrors": null
}
400
{ "data": null,
  "error": true,
  "errorText": "Something went wrong",
  "additionalErrors": null}

401 -- proxy: unauthorized
403
{ "data": null,
  "error": true,
  "errorText": "Ошибка авторизации",
  "additionalErrors": null}

"""
import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks/archive"
URL2 = "https://feedbacks-api.wb.ru/api/v1/feedbacks/archive"


async def feedback_get_archive_feedback_list(take: int,
                                             skip: int,
                                             nmId: int = None,
                                             order: str = None,
                                             ):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "take": take,
        "skip": skip,
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "take": 5000,
        "skip": 0,
    }

    pprint.pp(asyncio.run(feedback_get_archive_feedback_list(**sample_data)))
