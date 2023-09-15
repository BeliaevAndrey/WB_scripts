"""
Удалить шаблон
https://openapi.wildberries.ru/#tag/Shablony-dlya-voprosov-i-otzyvov/paths/~1api~1v1~1templates/delete

Метод позволяет удалить шаблон.

Request Body schema: application/json
templateID (REQUIRED) -- integer -- Идентификатор шаблона (max. 1)

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


async def answers_templates_post_create_template(templateID: int,):

    headers_dict = {
        "Authorization": __token
    }

    payload = {
        "templateID": templateID,
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.delete(url=URL, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_payload = {
        "templateID": 1,
    }

    pprint.pp(asyncio.run(answers_templates_post_create_template(**sample_payload)))
