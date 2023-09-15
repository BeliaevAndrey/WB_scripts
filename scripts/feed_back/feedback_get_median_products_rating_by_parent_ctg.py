"""
Средняя оценка товаров по родительской категории
https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1products~1rating/get

Метод позволяет получить среднюю оценку товаров по родительской категории.

Query parameters
subjectId (REQUIRED) -- integer Example: subjectId=3109 -- id категории товара


200
Response Schema: application/json
data -- Array of objects
Array[
    valuation -- integer -- Средняя оценка товаров
    feedbacksCount -- integer -- Количество отзывов по запрашиваемой категории
    ]
error -- boolean -- Есть ли ошибка
errorText -- string -- Описание ошибки
additionalErrors -- Array of strings or null -- Дополнительные ошибки

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

URL = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks/products/rating"
URL2 = "https://feedbacks-api.wb.ru/api/v1/feedbacks/products/rating"


async def feedback_get_median_products_rating_by_parent_ctg(subjectId: int):
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

    pprint.pp(asyncio.run(feedback_get_median_products_rating_by_parent_ctg(sample_id)))
