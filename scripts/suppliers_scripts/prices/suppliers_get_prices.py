"""
Получение информации о ценах.
https://openapi.wildberries.ru/#tag/Ceny/paths/~1public~1api~1v1~1info/get

Request samples
{
  "nmId": 1234567,
  "price": 1000,
  "discount": 10,
  "promoCode": 5
}

No response samples
"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/public/api/v1/info"


async def a_get_supp_obtain_prices(quantity: int = 0, **kwargs):
    headers = {
        'Authorization': __token,
    }

    params = {
        'quantity': quantity,
    }

    if kwargs:
        params.update(kwargs)

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_req = {
        "nmId": 1234567,
        "price": 1000,
        "discount": 10,
        "promoCode": 5
    }
    pprint.pp(asyncio.run(a_get_supp_obtain_prices(**sample_req)))
