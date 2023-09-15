"""
Работа с отзывом
https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks/patch



В зависимости от тела запроса можно:
    Просмотреть отзыв.
    Ответить на отзыв, или отредактировать ответ.

Отредактировать ответ на отзыв можно в течение 2 месяцев (60 дней),
после предоставления ответа и только 1 раз.

Request Body schema: application/json
One of
{
id (REQUIRED) -- string -- Id отзыва
wasViewed (REQUIRED) -- boolean Просмотрен (true), не просмотрен (false)
}

or
{
id (REQUIRED) -- string -- Id отзыва
text(REQUIRED) -- string -- Текст ответа (max. 999 символов)
}

Response samples
200 -- успешно

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
404
{ "data": null,
  "error": true,
  "errorText": "Не найден отзыв id",
  "additionalErrors": null}
"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"
URL2 = "https://feedbacks-api.wb.ru/api/v1/feedbacks"


async def feedback_patch_work_with_questions(feedback_id,
                                             text: str,
                                             wasViewed: bool = None,
                                             ):
    headers_dict = {
        "Authorization": __token
    }

    payload = {
        "id": feedback_id,
    }
    if wasViewed:
        payload.update(wasViewed=wasViewed)
    elif text:
        payload.update(text=text)
    print(payload)
    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.patch(url=URL, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "feedback_id": 1,
        "text": "Some text",
        "wasViewed": None,
    }

    pprint.pp(asyncio.run(feedback_patch_work_with_questions(**sample_data)))
