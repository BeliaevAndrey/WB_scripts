"""
Переименование кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie-Upravlenie-parametrami-kampanii/paths/~1adv~1v0~1rename/post

Метод позволяет переименовать кампанию.
Допускается максимум 300 запросов в минуту.

Request Body schema: application/json
advertId (REQUIRED) -- integer -- Идентификатор кампании, у которой меняется название
name (REQUIRED) -- string -- Новое название (максимум 100 символов)

Responses
200 -- Статус изменен
400 -- Неверная форма запроса
401 -- ошибка авторизации
422
"Ошибка обработки тела запроса"
"Ошибка изменения названия кампании"
"кампания не найдена или не принадлежит продавцу"

"""

import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/rename"


async def advance_param_post_rename_company(data):
    headers_dict = {
        "Authorization": __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "advertId": 2233344,
        "name": "newnmame"
    }

    pprint.pp(asyncio.run(advance_param_post_rename_company(sample_data)))
