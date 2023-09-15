"""
Список номенклатур для автоматической кампании
"https://openapi.wildberries.ru/#tag/Prodvizhenie-Upravlenie-parametrami-kampanii/paths/~1adv~1v1~1auto~1getnmtoadd/get"

Метод позволяет получать список номенклатур, доступных для добавления в кампанию.
Допускается максимум 60 запросов в минуту.

Query Parameters
id (REQUIRED) -- integer -- Идентификатор кампании

Responses
200 -- список доступных номенклатур
Response Schema: application/json
Array [
integer
]

400 -- '{"error":"кампания не найдена"}'
401 -- ошибка авторизации
429 -- превышен лимит запросов
"""

import aiohttp
import asyncio


from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/auto/getnmtoadd"


async def advance_param_get_param_auto_comp_nm_list(company_id):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "id": company_id
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint
    sample_data = {
        "company_id": 1,
    }
    pprint.pp(asyncio.run(advance_param_get_param_auto_comp_nm_list(**sample_data)))
