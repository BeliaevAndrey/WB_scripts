"""
Создание кампании, тестовый
https://openapi.wildberries.ru/#tag/Prodvizhenie-Testovyj-kontur/paths/~1adv~1v0~1adverts~1create/post

Метод позволяет создать кампании. new
Максимум можно создать 50 кампаний.

Метод создан исключительно для целей тестирования.
Метод позволяет создавать компании типа 4, 5, 6, 7, 9.
Для создания автоматических кампаний (тип 8) используется метод Создание кампании
Кампании (статус 4, 9, 11) будут удалены через 24 часа с момента внесения последних,
а завершенные кампании (статус 7) будут удалены через 1 час.

Статус кампании при создании - кампания на паузе (4).
Дневной бюджет(dailyBudget) при создании кампании равен 0.
Параметры menuId, menuName, subjectId, subjectName, setId, setName,
nm при создании кампании подставляются автоматически.
Флаг активности кампании и состояние номенклатуры при создании true.

Request Body schema: application/json
Array[
    type (REQUIRED) -- integer -- Тип кампании: 4 - кампания в каталоге;
                                  5 - кампания в карточке товара;
                                  6 - кампания в поиске
                                  7 - кампания в рекомендациях на главной странице;
                                  9 - поиск + каталог new
    startTime (REQUIRED) -- string -- Дата запуска кампании. Дата в формате RFC3339.
    endTime (REQUIRED) -- string -- Дата завершения кампании. Дата в формате RFC3339.
    name -- string -- Название кампании (max. 50)
    params -- (REQUIRED)-- Array of objects -- Параметры кампании.
                           Обязательный параметр для создания кампаний типов 4, 5, 6, 7.
                           Для создания кампаний типа 9 не используется.
    Array[
        intervals -- Array of objects -- Интервалы часов показа кампании (max. 24)
        Array[
            Begin -- integer -- Время начала показов
            End -- integer -- Время окончания показов
            price -- integer -- Текущая ставка. Для кампаний в каталоге, в
                                карточке товара и в поиске price >= 50.
                                Для кампаний в рекомендациях price >= 250.
            ]
        ]
]

Responses
200 -- успешно
400 -- неверный параметр
422 -- Ошибка обработки тела запроса
500
Превышен лимит на создание карточек, max = 50, создано = 51
or
За раз можно удалить 50 РК
or
Внутренняя ошибка сервиса

{
"code":404,
"message":"Error 9995b477-0d66ea6d392c-UK:88maoBRXeAn: path not found; Look at https://openapi.wb.ru/"
}
"""

import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v0/adverts/create"


async def advance_tst_cnt_post_create_campaign(data):
    headers_dict = {
        "Authorization": __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=data) as response:
            if response.status == 200:
                return await response.text()
            else:
                return response.status, await response.text()


if __name__ == '__main__':

    sample_data = [
        {
            "type": 4,
            "startTime": "2023-09-14T16:18:30",
            "endTime": "2023-09-14T18:18:30",
            "name": "FirstAdvert",
            "params": [
                {
                    "intervals": [
                        {
                            "Begin": 3,
                            "End": 20
                        }
                    ],
                    "price": 50
                },
                {
                    "intervals": [],
                    "dailyBudget": 1500,
                    "price": 234
                }
            ]
        },
        {
            "type": 5,
            "startTime": "2023-09-14T16:18:30",
            "endTime": "2023-09-14T18:18:30",
            "name": "FirstAdvert2",
            "params": [
                {
                    "intervals": [
                        {
                            "Begin": 3,
                            "End": 20
                        }
                    ],
                    "price": 50
                },
                {
                    "intervals": [],
                    "price": 234
                }
            ]
        },
        {
            "type": 6,
            "startTime": "2023-09-14T16:18:30",
            "endTime": "2023-09-14T18:18:30",
            "name": "FirstAdvert3",
            "params": [
                {
                    "intervals": [
                        {
                            "Begin": 3,
                            "End": 20
                        }
                    ],
                    "price": 50
                },
                {
                    "intervals": [],
                    "price": 234
                }
            ]
        },
        {
            "type": 7,
            "startTime": "2023-09-14T16:18:30",
            "endTime": "2023-09-14T18:18:30",
            "name": "FirstAdvert4",
            "params": [
                {
                    "intervals": [
                        {
                            "Begin": 3,
                            "End": 20
                        }
                    ],
                    "price": 250
                },
                {
                    "intervals": [],
                    "price": 250
                }
            ]
        },
        {
            "name": "Кампания9",
            "type": 9,
            "startTime": "2023-09-14T16:18:30",
            "endTime": "2023-09-14T18:18:30",
        }
    ]
    print(asyncio.run(advance_tst_cnt_post_create_campaign(sample_data)))

