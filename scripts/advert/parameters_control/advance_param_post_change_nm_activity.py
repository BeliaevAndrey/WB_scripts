"""
Изменение активности номенклатур кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie-Upravlenie-parametrami-kampanii/paths/~1adv~1v0~1nmactive/post

Метод позволяет изменить активность номенклатур только для кампании в поиске и рекомендациях и кампании в карточке товара.
В запросе необходимо передавать все номенклатуры кампании с их активностью, даже если изменение планируется только по одной номенклатуре.
При наличии в кампании нескольких subjectId номенклатуры по каждому subjectId необходимо передать отдельным запросом. То же касается setId.
Изменение активности номенклатур доступно для кампаний с типами 5, 6, 7.
Допускается максимум 300 запросов в минуту.


Request Body schema: application/json
advertId (REQUIRED) -- integer -- Идентификатор кампании.
active (REQUIRED) -- Array of objects -- Массив значений активности для номенклатур.
                                         Максимальноe количество номенклатур в запросе 50.
[
nm --integer -- Артикул WB (nmId)
active -- boolean -- Новое состояние
                    (true - сделать номенклатуру активной или
                    false - сделать номенклатуру неактивной)
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
"Активность номенклатур(-ы) не изменена"

"""

import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/nmactive"


async def advance_param_post_change_nm_activity(data):
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

    sample_data = {"advertId": 456789,
                   "active": [
                       {"nm": 2116745, "active": "true"},
                       {"nm": 301402, "active": "true"}
                   ],
                   "param": 275
                   }

    pprint.pp(asyncio.run(advance_param_post_change_nm_activity(sample_data)))
