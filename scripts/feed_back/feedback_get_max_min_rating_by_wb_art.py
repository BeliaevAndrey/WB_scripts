"""
Средняя оценка товара по артикулу WB
https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1products~1rating~1nmid/get

Метод позволяет получить среднюю оценку товара по его артикулу WB.

Query parameters
nmId (REQUIRED) -- integer Example: nmId=14917842 -- Артикул WB

200
Response samples:
{
  "data": {
    "valuation": "4.3",
    "feedbacksCount": 16
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

URL = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks/products/rating/nmid"
URL2 = "https://feedbacks-api.wb.ru/api/v1/feedbacks/products/rating/nmid"


async def feedback_get_max_min_rating_by_parent_ctg(nmId: int):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "nmId": nmId
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_nmid = 3109

    pprint.pp(asyncio.run(feedback_get_max_min_rating_by_parent_ctg(sample_nmid)))
