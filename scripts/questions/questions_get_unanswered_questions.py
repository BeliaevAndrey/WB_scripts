"""
Неотвеченные вопросы
https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1questions~1count-unanswered/get

Метод позволяет получить количество неотвеченных вопросов за сегодня и за всё время.

200
Response Schema: application/json
data -- object
{
hasNewQuestions -- boolean -- Есть ли непросмотренные вопросы (true есть, false нет)
hasNewFeedbacks -- boolean -- Есть ли непросмотренные отзывы (true есть, false нет)
}
error -- boolean -- Есть ли ошибка
errorText -- string -- Описание ошибки
additionalErrors -- Array of strings or null -- Дополнительные ошибки


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

URL = "https://feedbacks-api.wildberries.ru/api/v1/new-feedbacks-questions"
URL2 = "https://feedbacks-api.wb.ru/api/v1/new-feedbacks-questions"


async def questions_get_unanswered_questions():
    headers_dict = {
        "Authorization": __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    print(asyncio.run(questions_get_unanswered_questions()))
