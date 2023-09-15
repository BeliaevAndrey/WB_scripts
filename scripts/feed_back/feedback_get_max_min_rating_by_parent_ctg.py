"""
Средняя оценка товаров по родительской категории
https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1products~1rating/get

Метод позволяет получить среднюю оценку товаров по родительской категории.

Query parameters
subjectId (REQUIRED) -- integer Example: subjectId=3109 -- id категории товара


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

URL = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks/products/rating/top"
URL2 = "https://feedbacks-api.wb.ru/api/v1/feedbacks/products/rating/top"


async def feedback_get_max_min_rating_by_parent_ctg(subjectId: int):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "subjectId": subjectId
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_id = 3109

    pprint.pp(asyncio.run(feedback_get_max_min_rating_by_parent_ctg(sample_id)))
