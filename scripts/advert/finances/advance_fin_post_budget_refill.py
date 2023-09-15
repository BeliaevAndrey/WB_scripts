"""
Пополнение бюджета кампании
https://openapi.wildberries.ru/#tag/Prodvizhenie-Finansy/paths/~1adv~1v1~1budget~1deposit/post

Метод позволяет пополнять бюджет кампании.new
Допускается 1 запрос в секунду.

query Parameters
id (REQUIRED) -- integer -- Идентификатор кампании

Request Body schema: application/json
sum -- integer -- Сумма пополнения (min. 500 ₽)
type -- integer -- Тип источника пополнения: 0 - balance; 1 - net; 3 - bonus
Request sample
{ "sum": 500,
  "type": 1
}

Responses
200 -- Бюджет пополнен
400 -- Бюджет не пополнен

Response samples
{
  "error": "Сумма пополнения должна быть кратна 50 руб"
}

"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import adv_token as __token

URL = "https://advert-api.wb.ru/adv/v1/budget/deposit"


async def advance_fin_post_budget_refill(company_id: int, amount: int, source: int):
    headers_dict = {
        'Authorization': __token
    }

    params = {
        "id": company_id
    }

    payload = {
        "sum": amount,
        "type": source,
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, params=params, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        'company_id': 0,
        'amount': 0,
        'source': 0,
    }

    pprint.pp(asyncio.run(advance_fin_post_budget_refill(**sample_data)))
