"""
Список ставок по типу размещения кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie-Stavki/paths/~1adv~1v0~1allcpm/post

Метод позволяет получить список ставок по типу размещения кампании.
С помощью этого метода изменить ставку невозможно.

Допускается максимум 300 запросов в минуту.

query Parameters

type (REQUIRED) -- integer Enum: 4 5 6 7 -- кампании:
    4 - кампания в каталоге
    5 - кампания в карточке товара
    6 - кампания в поиске
    7 - кампания в рекомендациях на главной странице


Request Body schema: application/json

param -- Array of integers -- Массив параметров запроса, по которым будет получен список
                               ставок активных кампаний: должен быть значением menuId
                               (для кампании в каталоге), subjectId (для кампании в поиске и
                               рекомендациях) или setId (для кампании в карточке товара).

Responses
Array[
    param -- integer -- Значение параметра (param) запроса
    cpm -- Array of objects -- Информация о ставке(-ах)
Array
        [ Cpm -- integer -- Размер ставки
        Count -- integer -- Количество ставок ] ]

400
"Ошибка обработки тела запроса"
"Некорректный идентификатор продавца"

401 -- ошибка авторизации

"""

import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/allcpm"


async def advance_rates_get_cpm_list(company_type: int, data: list[int]):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "type": company_type
    }

    payload = {
        "type": data
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, params=params, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint
    sample_type = 5
    sample_data = [699, 344, 385]

    pprint.pp(asyncio.run(advance_rates_get_cpm_list(sample_type, sample_data)))
