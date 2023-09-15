"""
Изменение ставки у кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie-Stavki/paths/~1adv~1v0~1cpm/post

Изменение ставки у кампании.
Допускается максимум 300 запросов в минуту.

ВАЖНО! Если устанавливаемая ставка имеет размер меньше допустимого,
то в ответ Вы получите статус-код 422 (Размер ставки не изменён).
Информация об изменении минимального размера ставки публикуется в разделе Новости,
 на портале продавцов.

ВАЖНО! Принцип заполнения параметров type, instrument, param при изменении ставки
для кампании с типом 9 (поиск + каталог):
Для type указывается значение 9 (всегда).
Для instrument указывается значение 4 или 6 в зависимости от того, в каталоге
 или поиске необходимо изменить ставку.
Для param всегда указывается значение поля id из структуры subject ответа метода
"Информация о кампании", вне зависимости от того, в каталоге или поиске изменяется ставка.

ВАЖНО! Если в кампании Поиск + Каталог доступен только Поиск, то установить ставку в
Каталог (instrument = 4) не получится. В ответ Вы получите статус-код 422


Request Body schema: application/json
advertId (REQUIRED) -- integer -- Идентификатор кампании, где меняется ставка
type (REQUIRED) -- integer Enum: 5 6 7 8 9 -- кампании, где меняется ставка:
cpm (REQUIRED) -- integer -- Новое значение ставки
param (REQUIRED) -- integer -- Параметр, для которого будет внесено изменение. Является значением subjectId (для кампании в поиске и рекомендациях), setId (для кампании в карточке товара) или menuId (для кампании в каталоге).
Для автоматической кампании указывать этот параметр не требуется.
instrument -- integer -- тип кампании для изменения ставки в Поиск + Каталог (4 - каталог, 6 - поиск) new

Responses
200 -- размер ставки изменен

400
"Некорректное значение параметра param"
"Некорректное значение параметра type"
"Некорректное значение параметра cpm"
"Некорректный идентификатор продавца"

401 -- ошибка авторизации

422
"Размер ставки не изменен"
"Ошибка обработки тела запроса"
"кампания не найдена или не принадлежит продавцу"
"""

import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/cpm"


async def advance_rates_post_change_cpm(data):
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

    sample_data = {"advertId": 789,
                   "type": 5,
                   "cpm": 456,
                   "param": 23,
                   "instrument": 4}

    pprint.pp(asyncio.run(advance_rates_post_change_cpm(sample_data)))
