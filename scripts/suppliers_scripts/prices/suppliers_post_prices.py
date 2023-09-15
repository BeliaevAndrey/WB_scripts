"""
Загрузка цен
https://openapi.wildberries.ru/#tag/Ceny/paths/~1public~1api~1v1~1prices/post


Request Body schema: application/json
Array
nmId	integer     Номенклатура
price	    number  Цена (указывать без копеек)

Request samples
    [{
        "nmId": 1234567,
        "price": 1000
    }]


Response samples

200
Successful  -- Загрузка прошла успешно
{ "uploadId": 612455 }

Already exists  -- Загрузка с передаваемыми данными уже создана
{
  "uploadId": 123456789,
  "alreadyExists": true
}

400
{
  "error": [
    "No goods for process"
  ],
  "error_code": 1
}

{"errors":["incorrect data"]}

401
proxy: unauthorized
405
'See https://openapi.wb.ru'
"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/public/api/v1/prices"


async def a_get_supp_upload_prices(nmId: int, price: int):
    headers = {
        'Authorization': __token,
    }

    params = {
        "nmId": nmId,
        "price": price
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_req = {"nmId": 1, "price": 1}

    pprint.pp(asyncio.run(a_get_supp_upload_prices(**sample_req)))
