"""
Список НМ
https://openapi.wildberries.ru/#tag/Kontent-Prosmotr/paths/~1content~1v1~1cards~1cursor~1list/post

Метод позволяет получить список созданых НМ по фильтру
(баркод, артикул продавца, артикул WB (nmId), тег) с пагинацией и сортировкой.

Порядок работы с cursor/list:
Чтобы получить полный список номенклатур, если их > 1000, необходимо воспользоваться пагинацией.

1. Cделать первый запрос (все указанные ниже параметры обязательны):

    {"sort": {"cursor": {"limit": 1000},
              "filter": {"withPhoto": -1}}
    }

    По желанию можно добавить поиск по "textSearch" и сортировку.
    "sort": { "sortColumn": "", "ascending": false}

2. Пройти в конец полученного списка номенклатур, скопировать из cursor две строки:
3. Вставить скопированные строки в cursor запроса, повторить вызов метода.
4. Повторять пункты 2 и 3, пока total в ответе не станет меньше чем limit в запросе.
Это будет означать, что Вы получили все карточки.

Request sample

{
  "sort": {
    "cursor": {
      "updatedAt": "2022-09-23T17:41:32Z",
      "nmID": 66965444,
      "limit": 1000
    },
    "filter": {
      "textSearch": "test",
      "withPhoto": -1,
      "allowedCategoriesOnly": true
    },
    "sort": {
      "sortColumn": "updateAt",
      "ascending": false
    }
    }
}


Response Samples
200
{
"data": {
    "cards": [{...}],
    "cursor": {"updatedAt": "2022-08-10T10:16:52Z",
               "nmID": 66964167,
               "total": 1
               }
    },
    "error": false,
    "errorText": "",
    "additionalErrors": null
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

403
{
  "data": null,
  "error": true,
  "errorText": "Доступ запрещен",
  "additionalErrors": "Доступ запрещен"
}
"""

from __future__ import annotations
import aiohttp
import asyncio
from typing import Any

from wb_secrets import std_token as __token

URL = "https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list"


async def a_supp_post_p_card_cursor_list(data: dict) -> dict | tuple:
    headers_dict = {
        'Authorization': __token,
    }

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.post(url=URL, json=data) as request:
            if request.status == 200:
                return await request.json()
            else:
                return request.status, await request.text()


if __name__ == '__main__':
    import pprint

    sample_req = {
        "sort": {
            "cursor": {"updatedAt": "2022-09-23T17:41:32Z",
                       "nmID": 66965444,
                       "limit": 1000},
            "filter": {"textSearch": "test",
                       "withPhoto": -1,
                       "allowedCategoriesOnly": True},
            "sort": {"sortColumn": "updateAt",
                     "ascending": False}
        }
    }

    pprint.pp(asyncio.run(a_supp_post_p_card_cursor_list(sample_req)))

