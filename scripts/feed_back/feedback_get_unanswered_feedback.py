"""
Необработанные отзывы
https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1count-unanswered/get

Метод позволяет получить количество необработанных отзывов за сегодня,
за всё время, и среднюю оценку всех отзывов.


200
Response Schema: application/json
data -- object
{
countUnanswered --integer -- Количество необработанных отзывов
countUnansweredToday -- integer -- Количество необработанных отзывов за сегодня
valuation -- string -- Средняя оценка всех отзывов
}
error -- boolean -- Есть ли ошибка
errorText -- string -- Описание ошибки
additionalErrors -- Array of strings or null -- Дополнительные ошибки


401 -- authorization error

"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks/count-unanswered"
URL2 = "https://feedbacks-api.wb.ru/api/v1/feedbacks/count-unanswered"


async def feedback_get_unanswered_feedback():
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
    print(asyncio.run(feedback_get_unanswered_feedback()))
