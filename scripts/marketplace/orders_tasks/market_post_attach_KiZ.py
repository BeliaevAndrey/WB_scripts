"""
Закрепить за сборочным заданием КиЗ (маркировку Честного знака)
https://openapi.wildberries.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1{orderId}~1meta~1sgtin/post
Метод позволяет закрепить за сборочным заданием КиЗ (маркировку Честного знака). У одного сборочного задания не может быть больше 24 маркировок. Добавлять маркировку можно только для заказов в статусе confirm.

Параметры sid, numerator, denominator опциональны. Заполняются в зависимости от специфики товара.

ВАЖНО! Получить загруженные КиЗ можно только в личном кабинете. Для этого необходимо:

    Зайти в раздел Маркетплейс - Сборочные задания
    Пройти в любую из перечисленных вкладок (На сборке, В доставке, Архив)
    Зайти в детализацию поставки
    Нажать кнопку "Выгрузить в Excel"
    В полученном файле открыть лист КИЗы

Получить загруженные КиЗ можно по всем заказам, кроме: Новые, Отменено продавцом.

С правилами работы с КиЗ можно ознакомиться тут: https://честныйзнак.рф

О РЕАЛИЗАЦИИ API-ФУНКЦИОНАЛА ДЛЯ ПОЛУЧЕНИЯ ЗАГРУЖЕННЫХ КИЗ БУДЕТ
СООБЩЕНО В РАЗДЕЛЕ НОВОСТИ, НА ПОРТАЛЕ ПРОДАВЦОВ.

path Parameters
orderId(REQUIRED)   integer <int64>     ID сборочного задания

Request Body schema: application/json

stgin -- Array of objects -- [ 1 .. 24 ] items  Массив КиЗов.

[
    ([ 1 .. 24 ] items)
    code(REQUIRED) -- string [ 16 .. 135 ] -- Код маркировки на упаковке. От 16 до 135 символов.
]

Request samples
{
  "sgtin": [
    {
      "code": "1234567890123456"
    }
  ]
}
"""
#
# from __future__ import annotations
#
# import aiohttp
# import asyncio
#
# from wb_secrets import std_token as __token
#
# URL = "https://suppliers-api.wildberries.ru/api/v3/orders/{orderId}/meta/sgtin"
#
#
# async def market_post_attach_KiZ(data: dict[str, list[dict[str, str]]], orderId):
#     headers_dict = {
#         'Authorization': __token
#     }
#
#     async with aiohttp.ClientSession(headers=headers_dict) as session:
#         async with session.post(url=URL.format(orderId=orderId), json=data) as response:
#             if response.status == 200:
#                 return await response.json()
#             else:
#                 return response.status, await response.text()
#
#
# if __name__ == '__main__':
#     import pprint
#
#     sample_data = {"sgtin": [{"code": "1234567890123456"}]}
#     order_id = 5632423
#     pprint.pp(asyncio.run(market_post_attach_KiZ(sample_data, order_id)))
