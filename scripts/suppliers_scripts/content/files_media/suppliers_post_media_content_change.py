"""
Изменение медиа контента КТ
https://openapi.wildberries.ru/#tag/Kontent-Mediafajly/paths/~1content~1v1~1media~1file/post
Метод позволяет загрузить и добавить один медиафайл за запрос, к НМ в КТ.
Требования к медиафайлам:
Фото: минимальное разрешение – 450х450.
Максимально допустимое количество фото в КТ 30.
Допустимые форматы изображений - jpg и png.
Видео: максимальный размер 50 мб. Форматы MOV, MP4.
Максимально допустимое количество видео в КТ 1.

Header Parameters
X-Vendor-Code (required)         string      Артикул продавца
X-Photo-Number (required)       integer     Example: 2
                                            Номер медиафайла на загрузку. Начинать с 1.
                                            При загрузке видео всегда указывать значение 1.
                                            Чтобы добавить фото к уже загруженным в НМ,
                                            номер медиафайла должен быть больше кол-ва
                                            загруженных в НМ медиафайлов.

Request Body schema: multipart/form-data
uploadfile      string <binary>

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
import os

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/content/v1/media/file"


async def a_supp_post_media_add(vendorCode: str, x_photo_number: int, file_path: str) -> dict | tuple:
    headers_dict = {
        'Authorization': __token,
        'X-Vendor-Code': vendorCode,
        'X-Photo-Number': str(x_photo_number),
        'Content-Type': 'multipart/form-data',
    }

    if not os.path.exists(file_path):
        return 0, "File not found"

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        form = aiohttp.FormData()
        form.add_field('file', open(file_path, 'rb'), content_type='image/png')
        async with session.post(url=URL, data=form) as request:
            if request.status == 200:
                return await request.json()
            else:
                return request.status, await request.text()


if __name__ == '__main__':
    import pprint
    file_path = '/large/data2/Home/Andrew/Desktop/unix_book_snap.png'
    pprint.pp(asyncio.run(a_supp_post_media_add('6000000001', 2, file_path)))
