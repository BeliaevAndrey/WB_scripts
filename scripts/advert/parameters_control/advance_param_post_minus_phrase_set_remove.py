"""
Установка/удаление минус-фраз фразового соответствия для кампании в поиске
https://openapi.wildberries.ru/#tag/Prodvizhenie-Upravlenie-parametrami-kampanii/paths/~1adv~1v1~1search~1set-phrase/post

Метод позволяет устанавливать и удалять фиксированные фразы.
Отправка пустого массива удаляет все фиксированные фразы и отключает активность
фиксированных фраз в кампании.
Допускается 2 запроса в секунду.

query Parameters
id (REQUIRED) -- integer -- Идентификатор кампании

Request Body schema: application/json
phrase -- Array of strings -- Минус-фразы

Responses
200 -- Успешно

400 -- некорректный запрос
401 -- ошибка авторизации

"""

import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/search/set-phrase"


async def advance_param_post_minus_phrase_set_remove(company_id: int,
                                               phrase: list[str],
                                               ):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "id": company_id,
    }

    payload = {
        "phrase": phrase
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
        "phrase": ["сло",
                   "гу"]
    }

    pprint.pp(asyncio.run(advance_param_post_minus_phrase_set_remove(sample_id, **sample_data)))
