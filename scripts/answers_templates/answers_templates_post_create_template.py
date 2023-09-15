"""
Создать шаблон
https://openapi.wildberries.ru/#tag/Shablony-dlya-voprosov-i-otzyvov/paths/~1api~1v1~1templates/post

Метод позволяет создать шаблон ответа на отзыв/вопрос. new
Всего можно создать 20 шаблонов. 10 на отзывы и 10 на вопросы.
Допустимы любые символы.

Request Body schema: application/json
name (REQUIRED) -- string -- Название шаблона (от 1 до 100 символов)
templateType (REQUIRED) -- integer -- Тип шаблона: 1 - шаблон для отзывов; 2 - шаблон для вопросов
text (REQUIRED) -- string -- Текст шаблона (от 2 до 1000 символов)


Response samples:
200

{
  "data": {
    "id": "1234"
  },
  "error": false,
  "errorText": "",
  "additionalErrors": null
}
or
{
  "data": null,
  "error": true,
  "errorText": "Описание ошибки",
  "additionalErrors": null
}

401
{Error ae394f96-e258-432d-af13-a53a3d31f8b0:
request rejected, unathorized: 1;
empty Authorization header}
or
{Error ae394f96-e258-432d-af13-a53a3d31f8b0: request rejected,
unathorized: token scope not allowed for this API route}

"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://feedbacks-api.wildberries.ru/api/v1/templates"
URL2 = "https://feedbacks-api.wb.ru/api/v1/templates"


async def answers_templates_post_create_template(name: str,
                                                 templateType: int,
                                                 text: str,
                                                 ):
    headers_dict = {
        "Authorization": __token
    }

    payload = {
        "name": name,
        "templateType": templateType,
        "text": text
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_payload = {
        "name": "name",
        "templateType": 1,
        "text": "text"
    }

    pprint.pp(asyncio.run(answers_templates_post_create_template(**sample_payload)))
