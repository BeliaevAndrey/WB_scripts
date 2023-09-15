"""
Получить отзыв по Id
https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedback/get

Метод позволяет получить количество вопросов. new


Query Parameters
id (REQUIRED) -- string Example: id=G7Y9Y1kBAtKOitoBT_lV -- Идентификатор отзыва


200
Response samples:
{ "data": 77,
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

422,
{ "data":null,"error":true,"errorText":"Не удалось получить отзыв по данному ID",
  "additionalErrors":null,
  "requestId":"f36b4f3b-3719-48e9-8e8c-bb033e48f7cd"}
"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://feedbacks-api.wildberries.ru/api/v1/feedback"
URL2 = "https://feedbacks-api.wb.ru/api/v1/feedback"


async def feedback_get_feedback_quantity(feedback_id: str):
    headers_dict = {
        "Authorization": __token
    }

    params = {"id": feedback_id}

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {'feedback_id': "G7Y9Y1kBAtKOitoBT_lV"}

    pprint.pp(asyncio.run(feedback_get_feedback_quantity(**sample_data)))
