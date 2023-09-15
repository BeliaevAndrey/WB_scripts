"""
Изменение интервалов показа кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie-Upravlenie-parametrami-kampanii/paths/~1adv~1v0~1intervals/post

Метод позволяет изменить временной интервал показа кампании.
Изменение интервалов доступно для кампаний с типами:
4 - кампании в каталоге new
5 - кампании в карточке товара
6 - кампании в поиске
7 - кампании в рекомендациях
Допускается максимум 300 запросов в минуту

Request Body schema: application/json
advertId (REQUIRED) -- integer -- Идентификатор кампании.
(REQUIRED) -- Array of objects
Массив новых значений для интервалов.Максимальное количество интервалов 24.
[
begin -- integer -- Время начала показов, по 24 часовой схеме ("begin": 15)
end -- integer -- Время окончания показов, по 24 часовой схеме ("end": 21)
]

param(REQUIRED) -- integer -- Параметр, для которого будет внесено изменение.
                              Должен быть значением subjectId (для кампании в поиске и рекомендациях),
                              setId (для кампании в карточке товара) или
                              menuId (для кампании в каталоге)

Responses
200 -- Статус изменен
400 -- Неверная форма запроса
401 -- ошибка авторизации
422
"Ошибка обработки тела запроса"
"Ошибка изменения интервалов показа"
"Интервалы показов кампании не изменены"

"""

import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/intervals"


async def advance_param_post_change_show_intervals(data):
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
        "advertId": 3344123,
        "intervals": [{"begin": 3, "end": 5}, {"begin": 19, "end": 21}],
        "param": 275
    }

    pprint.pp(asyncio.run(advance_param_post_change_show_intervals(sample_data)))
