"""
Родительские категории товаров
https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1parent-subjects/get

Метод позволяет получить список родительских категорий товаров, которые есть у продавца.

Query Parameters
size(REQUIRED) -- integer -- Количество запрашиваемых товаров (max. 100)

200
Response samples:
{
  "data": [
    {
      "subjectId": 1162,
      "subjectName": "Строительные инструменты"
    }
  ],
  "error": false,
  "errorText": "",
  "additionalErrors": null
}

400
{ "data": null,
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

URL = "https://feedbacks-api.wildberries.ru/api/v1/parent-subjects"
URL2 = "https://feedbacks-api.wb.ru/api/v1/parent-subjects"


async def feedback_get_parent_categories_of_goods():
    headers_dict = {
        "Authorization": __token
    }

    params = {}

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    pprint.pp(asyncio.run(feedback_get_parent_categories_of_goods()))
