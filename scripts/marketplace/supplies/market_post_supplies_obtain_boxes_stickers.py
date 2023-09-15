"""
Получить стикеры коробов поставки
https://openapi.wildberries.ru/#tag/Marketplace-Postavki/paths/~1api~1v3~1supplies~1{supplyId}~1trbx~1stickers/post

Возвращает стикеры QR в svg, zplv (вертикальный), zplh (горизонтальный), png.
Можно получить, только если в коробе есть заказы.
Размер стикеров: 580x400 пикселей

path Parameters
supplyId (REQUIRED) -- string -- ID поставки

Request Body schema: application/json
name -- string [ 1 .. 128 ] characters -- Наименование поставки

query Parameters
type (REQUIRED) -- string -- Enum: "svg" "zplv" "zplh" "png" -- Тип этикетки

Request Body schema: application/json
trbxIds (REQUIRED) -- Array of strings -- Список ID коробов, по которым необходимо вернуть стикеры.

Request samples
{
  "trbxIds": ["WB-TRBX-1234567"]
}

Response Schema: application/json
id -- string -- Идентификатор поставки

Response samples
200
{
  "stickers": [{
      "barcode": "$WBMP:1:123:1234567",
      "file": "U3dhZ2dlciByb2Nrcw=="
      }]
}

400
{ "code": "IncorrectParameter",
  "message": "Передан некорректный параметр"}

401
proxy: unauthorized     -- Токен отсутствует
or
proxy: invalid token    -- Токен недействителен
or
proxy: not found        -- Токен удален

403
{ "code": "AccessDenied",
  "message": "Доступ запрещён"}

429 -- превышен лимит по запросам

500
{ "code": "InternalServerError",
  "message": "Внутренняя ошибка сервиса"}
"""
from __future__ import annotations

import aiohttp
import asyncio
import json

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/supplies/{supplyId}/trbx/stickers"


async def market_post_supplies_obtain_boxes_stickers(supplyId: str,
                                                     sticker_type: str,
                                                     trbxIds: list[str],
                                                     ) -> list[list[dict]] | tuple:
    headers_dict = {
        'Authorization': __token
    }
    params = {
        "type": sticker_type
    }
    payload = {
        "trbxIds": trbxIds
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL.format(supplyId=supplyId),
                                params=params,
                                json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    data = {
        "supplyId": "WB-GI-57989471",
        "sticker_type": "svg",
        "trbxIds": ["WB-TRBX-1234567"]
    }

    pprint.pp(asyncio.run(market_post_supplies_obtain_boxes_stickers(**data)))
