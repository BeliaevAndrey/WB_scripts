"""
Изменение активности предметной группы для кампании в поиске
https://openapi.wildberries.ru/#tag/Prodvizhenie-Upravlenie-parametrami-kampanii/paths/~1adv~1v0~1active/get

Метод позволяет изменить активность предметной группы для кампании в поиске.
Изменение активности доступно только для кампании в статусе 9 или 11.
Допускается максимум 60 запросов в минуту.

query Parameters
id (REQUIRED) -- integer -- Идентификатор кампании
subjectId (REQUIRED) -- integer -- Идентификатор предметной группы, для которой меняется активность
status (REQUIRED) -- string -- Новое состояние (true - сделать группу активной или false - сделать группу неактивной)

Responses
200 -- Статус изменен

400 -- Статус не изменен
401 -- ошибка авторизации
422 -- "Активность предметной группы не изменена"

"""

import aiohttp
import asyncio


from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/active"


async def advance_param_get_change_activity_subj_group(company_id: int, subjectId: int, status: str):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "id": company_id,
        "subjectId": subjectId,
        "status": status,
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
        "company_id": 1234,
        "subjectId": 1234,
        "status": "true"
    }
    pprint.pp(asyncio.run(advance_param_get_change_activity_subj_group(**sample_data)))
