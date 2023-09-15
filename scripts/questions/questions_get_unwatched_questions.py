"""
Непросмотренные отзывы и вопросы
https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1new-feedbacks-questions/get

Метод отображает информацию о наличии у продавца непросмотренных отзывов и вопросов.
200
Response Schema: application/json
data -- object
{
countUnanswered -- integer -- Количество неотвеченных вопросов
countUnansweredToday -- integer -- Количество неотвеченных вопросов за сегодня
}
error -- boolean -- Есть ли ошибка
errorText -- string -- Описание ошибки
additionalErrors -- Array of strings or null -- Дополнительные ошибки

"""
import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://feedbacks-api.wildberries.ru/api/v1/questions/count-unanswered"
URL2 = "https://feedbacks-api.wb.ru/api/v1/questions/count-unanswered"


async def questions_get_unwatched_questions():
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
    print(asyncio.run(questions_get_unwatched_questions()))
