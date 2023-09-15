"""
Установка/удаление фиксированных фраз у кампании в поиске
https://openapi.wildberries.ru/#tag/Prodvizhenie-Upravlenie-parametrami-kampanii/paths/~1adv~1v1~1search~1set-plus/post

Метод позволяет устанавливать и удалять фиксированные фразы.
Отправка пустого массива удаляет все фиксированные фразы и отключает активность
фиксированных фраз в кампании.
Допускается 2 запроса в секунду.

query Parameters
id (REQUIRED) -- integer -- Идентификатор кампании

Request Body schema: application/json
pluse -- Array of strings -- Список фиксированных фраз (max. 100)

Responses
200 -- Успешно
response sample:
[ "Фраза 1",
  "Фраза 2"]

400 -- некорректный запрос
401 -- ошибка авторизации

"""

import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/search/set-plus"


async def advance_param_post_change_show_intervals(company_id: int,
                                             pluse: list[str],
                                             ):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "id": company_id,
    }

    payload = {
        "pluse": pluse
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, params=params, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_id = 1

    sample_data = {
        "pluse": ["Фраза 1",
                  "Фраза 2"]
    }

    pprint.pp(asyncio.run(advance_param_post_change_show_intervals(sample_id, **sample_data)))
