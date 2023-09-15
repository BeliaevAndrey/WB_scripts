"""
Изменение медиа контента КТ
https://openapi.wildberries.ru/#tag/Kontent-Mediafajly/paths/~1content~1v1~1media~1save/post
Метод позволяет изменить порядок изображений или удалить медиафайлы с НМ в КТ,
а также загрузить изображения в НМ со сторонних ресурсов по URL.
Текущие изображения заменяются на переданные в массиве data.

Требования к медиафайлам:
Фото: минимальное разрешение – 450х450.
Максимально допустимое количество фото в КТ 30.
Допустимые форматы изображений - jpg и png.

Если хотя бы одно изображение в запросе не соответствует требованиям к
медиафайлам, то даже при коде ответа 200 ни одно изображение не загрузится в КТ.

Request Body schema: application/json
vendorCode      string              Артикул продавца
data            Array of strings    Ссылки на изображения в том порядке,
                                    в котором мы хотим их увидеть в карточке товара.

Request samples
{
  "vendorCode": "6000000001",
  "data": [
    "https://basket-stage-02.wb.ru/vol669/part66964/66964260/images/big/2.jpg"
  ]
}

200
{
  "data": null,
  "error": false,
  "errorText": "",
  "additionalErrors": ""
}

400
{
  "data": null,
  "error": true,
  "errorText": "Текст ошибки",
  "additionalErrors": {
    "MoveNmsToTrash": "Bad request"
  }
}

401
proxy: unauthorized

"""

from __future__ import annotations
import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/content/v1/media/save"


async def a_supp_post_media_change(vendorCode: str, data: list[str]) -> dict | tuple:
    headers_dict = {
        'Authorization': __token
    }

    params = {
        'vendorCode': vendorCode,
        'data': data
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=params) as request:
            if request.status == 200:
                return await request.json()
            else:
                return request.status, await request.text()


if __name__ == '__main__':
    import pprint

    sample_req = {
        "vendorCode": "6000000001",
        "data": ["https://basket-stage-02.wb.ru/vol669/part66964/66964260/images/big/2.jpg"]
    }

    pprint.pp(asyncio.run(a_supp_post_media_change(**sample_req)))

# (400,
#  '{"additionalErrors":null,"data":null,"error":true,"errorText":"Ошибка '
#  'сохранения продукта: ошибки для всех ссылок: [\\"creating tempfile from '
#  'url=https://basket-stage-02.wb.ru/vol669/part66964/66964260/images/big/2.jpg: '
#  'downloading file: sending HTTP GET request with timeout=15s: error sending '
#  'request for url '
#  '(https://basket-stage-02.wb.ru/vol669/part66964/66964260/images/big/2.jpg): '
#  'error trying to connect: unsuccessful tunnel\\"]"}')
