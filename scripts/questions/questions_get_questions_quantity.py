"""
Количество вопросов
https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1questions~1count/get

Метод позволяет получить количество вопросов. new


Query Parameters
dateFrom -- integer -- Дата начала периода в формате Unix timestamp
dateTo -- integer -- Дата конца периода в формате Unix timestamp
isAnswered -- boolean -- Обработанные вопросы(true) или необработанные вопросы(false).
                         Если не указать, вернутся обработанные вопросы.

200
Response samples:
{
  "data": 77,
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

"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://feedbacks-api.wildberries.ru/api/v1/questions/count"
URL2 = "https://feedbacks-api.wb.ru/api/v1/questions/count"


async def questions_get_questions_quantity(dateFrom: int = None,
                                           dateTo: int = None,
                                           isAnswered: str = None,
                                           ):
    headers_dict = {
        "Authorization": __token
    }

    params = {}
    if dateFrom:
        params.update(dateFrom=dateFrom)
    if dateTo:
        params.update(dateTo=dateTo)
    if isAnswered:
        params.update(isAnswered=isAnswered)

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    pprint.pp(asyncio.run(questions_get_questions_quantity()))
