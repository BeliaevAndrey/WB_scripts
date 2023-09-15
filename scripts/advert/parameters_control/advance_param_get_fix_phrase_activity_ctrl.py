"""
Управление активностью фиксированных фраз у кампании в поиске
https://openapi.wildberries.ru/#tag/Prodvizhenie-Upravlenie-parametrami-kampanii/paths/~1adv~1v1~1search~1set-plus/get

Метод позволяет изменять активность фиксированных фраз у кампании в поиске.
Допускается 2 запроса в секунду.

Query Parameters
id (REQUIRED) -- integer -- Идентификатор кампании
fixed -- boolean -- Новое состояние (false - сделать неактивными, true - сделать активными)

Responses
200 -- Активность изменена

400 -- Активность не изменена
401 -- ошибка авторизации

"""

import aiohttp
import asyncio


from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/search/set-plus"


async def advance_param_get_fix_phrase_activity_ctrl(company_id: int, fixed: str):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "id": company_id,
        "fixed": fixed,
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
        "fixed": "true"
    }
    pprint.pp(asyncio.run(advance_param_get_fix_phrase_activity_ctrl(**sample_data)))

