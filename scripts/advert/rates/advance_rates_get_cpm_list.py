"""
Список ставок
https://openapi.wildberries.ru/#tag/Prodvizhenie-Stavki/paths/~1adv~1v0~1cpm/get

Получение списка ставок для типа размещения.
Данные в ответе отсортированы по величине ставки от большей к меньшей.
Допускается максимум 300 запросов в минуту.

query Parameters
type (REQUIRED) -- integer Enum: 4 5 6 7 -- кампании:
    4 - кампания в каталоге
    5 - кампания в карточке товара
    6 - кампания в поиске
    7 - кампания в рекомендациях на главной странице
param (REQUIRED) -- integer -- Параметр запроса, по которому будет получен список
                               ставок активных кампаний.
                               Должен быть значением menuId, subjectId или setId в
                               зависимости от типа кампании. Получить их можно методом
                               Информация о кампании

Responses
200
Response Schema: application/json
Array [
Cmp -- integer -- Размер ставки
Count -- integer -- Количество ставок
]

400
"Некорректное значение параметра param"
"Некорректное значение параметра type"
"Некорректный идентификатор продавца"

401 -- ошибка авторизации

422
"Размер ставки не изменен"
"Ошибка обработки тела запроса"

"""
import aiohttp
import asyncio


from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/cpm"


async def advance_rates_get_cpm_list(data):
    headers_dict = {
        "Authorization": __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint
    sample_data = {
        "type": 4,
        "param": 1234,
    }
    pprint.pp(asyncio.run(advance_rates_get_cpm_list(sample_data)))
