"""
Работа с вопросами
https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1questions/patch


В зависимости от тела запроса можно:
    Просмотреть вопрос.
    Отклонить вопрос.
    Ответить на вопрос или отредактировать ответ.

Отредактировать ответ на вопрос можно в течение 2 месяцев (60 дней),
после предоставления ответа и только 1 раз.

Request Body schema: application/json
One of
{
id (REQUIRED) -- string -- Id вопроса
wasViewed (REQUIRED) -- boolean Просмотрен (true), не просмотрен (false)
}

or
{
id (REQUIRED) -- string -- Id вопроса
answer (REQUIRED) -- object
    {
    text(REQUIRED) -- string -- Текст ответа
    }
state(REQUIRED)string -- Статус вопроса (none) - вопрос отклонён продавцом (такой вопрос не отображается на портале покупателей).
}

or
{
id (REQUIRED)string -- Id вопроса
answer (REQUIRED) -- object
    {
    text (REQUIRED) -- string -- Текст ответа
    }
state (REQUIRED) -- string -- Статус вопроса (wbRu) - ответ предоставлен, вопрос отображается на сайте покупателей.
}

Response samples
200
{
  "data": {
    "fileName": "report.xlsx",
    "file": "UEsDBBQAC ... CAADMdQAAAAA=",
    "contentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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
404
{ "data": null,
  "error": true,
  "errorText": "Не найден отзыв id",
  "additionalErrors": null}
"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://feedbacks-api.wildberries.ru/api/v1/questions"
URL2 = "https://feedbacks-api.wb.ru/api/v1/questions"


async def questions_patch_work_with_questions(question_id,
                                              answer: dict = None,
                                              state: str = None,
                                              wasViewed: str = None,
                                              ):
    headers_dict = {
        "Authorization": __token
    }

    payload = {
        "id": question_id,
    }
    if wasViewed:
        payload.update(wasViewed=wasViewed)
    elif answer and answer.get("text"):
        payload.update(answer=answer)
        if state:
            payload.update(state=state)

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.patch(url=URL, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "question_id": 1,
        "answer": {"text": None},
        "state": None,
        "wasViewed": True,
    }

    pprint.pp(asyncio.run(questions_patch_work_with_questions(**sample_data)))
