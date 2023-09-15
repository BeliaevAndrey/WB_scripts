"""
Установка/удаление минус-фраз из поиска для кампании в поиске
https://openapi.wildberries.ru/#tag/Prodvizhenie-Upravlenie-parametrami-kampanii/paths/~1adv~1v1~1search~1set-excluded/post

Метод позволяет устанавливать/удалять минус-фразы из поиска. new
Отправка пустого массива удаляет все минус-фразы из поиска из кампании.

query Parameters
id (REQUIRED) -- integer -- Идентификатор кампании

Request Body schema: application/json
excluded -- Array of strings -- Минус-фразы

Responses
200 -- Успешно

400 -- некорректный запрос
401 -- ошибка авторизации

"""

import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/search/set-excluded"


async def advance_param_post_minus_phrase_searched_set_remove(company_id: int,
                                                        excluded: list[str],
                                                        ):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "id": company_id,
    }

    payload = {
        "excluded": excluded
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
        "excluded": ["что-то синее", "картошечка"]
    }

    pprint.pp(asyncio.run(advance_param_post_minus_phrase_searched_set_remove(sample_id, **sample_data)))
