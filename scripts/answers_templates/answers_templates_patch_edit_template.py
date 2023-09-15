"""
Редактировать шаблон
https://openapi.wildberries.ru/#tag/Shablony-dlya-voprosov-i-otzyvov/paths/~1api~1v1~1templates/patch

Метод позволяет отредактировать шаблон. new
Допустимы любые символы.

Request Body schema: application/json
name (REQUIRED) -- string -- Название шаблона (от 1 до 100 символов)
templateID (REQUIRED) -- integer -- Идентификатор шаблона

text (REQUIRED) -- string -- Текст шаблона (от 2 до 1000 символов)


Response samples:
200

data -- boolean or null
error -- boolean -- Есть ли ошибка
errorText -- string -- Описание ошибки
additionalErrors -- Array of strings or null -- Дополнительные ошибки


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
                                                 templateId: str,
                                                 text: str,
                                                 ):
    headers_dict = {
        "Authorization": __token
    }

    payload = {
        "name": name,
        "templateId": templateId,       # str(hex(int)) e.g.: 65033fd63b20ac27ae163e2b
        "text": text
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.patch(url=URL, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_payload = {
        "name": "name changed",
        "templateId": "65033fd63b20ac27ae163e2b",
        "text": "text edited"
    }

    pprint.pp(asyncio.run(answers_templates_post_create_template(**sample_payload)))
