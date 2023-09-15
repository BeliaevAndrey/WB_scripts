"""
Управление зонами показов в автоматической кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie-Upravlenie-parametrami-kampanii/paths/~1adv~1v1~1auto~1active/post

Метод позволяет изменять активность зон показов. new
Допускается максимум 60 запросов в минуту.
Вы можете осуществлять показы товаров во всех зонах либо выборочно.

query Parameters
id (REQUIRED) -- integer -- Идентификатор кампании

recom -- boolean -- Рекомендации на главной (false - отключены, true - включены)
booster -- boolean -- Поиск/Каталог (false - отключены, true - включены)
carousel -- boolean -- Карточка товара (false - отключены, true - включены)

Responses
200 -- Успешно
400 -- "не удалось получить активность инструментов продвижения"
401 -- ошибка авторизации
429 -- Превышен лимит запросов

"""

import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/auto/active"


async def advance_param_post_show_zones_control(company_id: int,
                                             recom: bool,
                                             booster: bool,
                                             carousel: bool
                                             ):
    headers_dict = {
        "Authorization": __token
    }

    params = {
        "id": company_id,
    }

    payload = {
        "recom": recom,
        "booster": booster,
        "carousel": carousel,
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
        "recom": True,
        "booster": True,
        "carousel": True
    }

    pprint.pp(asyncio.run(advance_param_post_show_zones_control(sample_id, **sample_data)))
