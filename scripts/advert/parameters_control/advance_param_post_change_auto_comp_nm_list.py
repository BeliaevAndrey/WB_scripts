"""
Изменение списка номенклатур в автоматической кампании
Изменение списка номенклатур в автоматической кампании

Метод позволяет добавлять и удалять номенклатуры. new
Допускается максимум 60 запросов в минуту.
Важно: Добавить можно только те номенклатуры, которые
вернутся в ответе метода "Список номенкатур для автоматической кампании".
Удалить единственную номенклатуру из кампании нельзя.
Проверки по параметру delete не предусмотрено.
Если пришел ответ со статус-кодом 200, а изменений не произошло, то проверьте
запрос на соответствие документации.

Query Parameters
id (REQUIRED) -- integer -- Идентификатор кампании

Request Body schema: application/json
add -- Array of integers -- Номенклатуры, которые необходимо добавить.
delete -- Array of integers -- Номенклатуры, которые необходимо удалить.


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

URL = "https://advert-api.wb.ru/adv/v1/auto/updatenm"


async def advance_param_post_change_auto_comp_nm_list(comp_id: int, data: dict):
    headers_dict = {
        "Authorization": __token
    }
    params = {
        "id": comp_id
    }
    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_id = 1
    sample_data = {"add": [11111111, 44444444],
                   "delete": [55555555]
                   }

    pprint.pp(asyncio.run(advance_param_post_change_auto_comp_nm_list(sample_id, sample_data)))
