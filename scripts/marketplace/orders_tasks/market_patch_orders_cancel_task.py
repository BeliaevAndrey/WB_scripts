"""
Отменить сборочное задание
https://openapi.wildberries.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1{orderId}~1cancel/patch

Переводит сборочное задание в статус cancel ("Отменено продавцом").

Path Parameters
orderId -- (REQUIRED) -- integer <int64> -- ID сборочного задания

Responses
204 -- отменено

"""
from __future__ import annotations

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/api/v3/orders/{orderId}/cancel"


async def market_post_orders_status(orderId: int):

    headers_dict = {
        'Authorization': __token
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.patch(url=URL.format(orderId=orderId)) as response:
            if response.status == 204:
                return await response.json()
            else:
                return response.status, await response.text()


