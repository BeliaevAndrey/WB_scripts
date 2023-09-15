"""
Получить шаблоны ответов
https://openapi.wildberries.ru/#tag/Shablony-dlya-voprosov-i-otzyvov/paths/~1api~1v1~1templates/get

query Parameters
templateType (REQUIRED) -- integer -- Example: templateType=1
1 - шаблоны для отзывов
2 - шаблоны для вопросов

Response samples:
{ "data": {
    "templates": [
      { "id": "id",
        "name": "name",
        "text": "text"
      }]
  },
  "error": false,
  "errorText": "",
  "additionalErrors": {}
  }
or
{
  "data": null,
  "error": true,
  "errorText": "Неизвестный тип шаблона",
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


async def answers_templates_get_templates(templateType: int):
    headers_dict = {
        "Authorization": __token
    }

    params = {"templateType": templateType}

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_type = 1

    pprint.pp(asyncio.run(answers_templates_get_templates(sample_type)))
