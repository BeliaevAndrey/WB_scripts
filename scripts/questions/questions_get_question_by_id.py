"""
Получить вопрос по Id
https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1question/get

Метод позволяет получить вопрос по его Id.


Query Parameters
id (REQUIRED) -- string -- Example: id=K40ZY1kBHA64Ev-ch5bd -- Идентификатор вопроса



200
Response samples:
{
  "data": {
    "id": "string",
    "text": "string",
    "createdDate": "2019-08-24T14:15:22Z",
    "state": "string",
    "answer": {
      "text": "string",
      "editable": true,
      "createDate": "2019-08-24T14:15:22Z"
    },
    "productDetails": {
      "nmId": 0,
      "imtId": 0,
      "productName": "string",
      "supplierArticle": "string",
      "supplierName": "string",
      "brandName": "string"
    },
    "wasViewed": true
  },
  "error": false,
  "errorText": "",
  "additionalErrors": null
}

400
{   "data": null,
    "error": true,
    "errorText": "Something went wrong",
    "additionalErrors": null}
401 -- authorization error
403
{ "data": null,
  "error": true,
  "errorText": "Ошибка авторизации",
  "additionalErrors": null}

422,
 '{"data":null,"error":true,"errorText":"Не удалось получить вопрос по данному '
 'ID","additionalErrors":null,"requestId":"74387b33-aca9-43aa-ad64-24ede28fb09c"}
"""

import aiohttp
import asyncio

from wb_secrets import std_token as __token

URL = "https://feedbacks-api.wildberries.ru/api/v1/question"
URL2 = "https://feedbacks-api.wb.ru/api/v1/question"


async def questions_get_question_by_id(question_id: str):
    headers_dict = {
        "Authorization": __token
    }

    params = {"id": question_id}

    async with aiohttp.ClientSession(headers=headers_dict) as session:
        async with session.get(url=URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return response.status, await response.text()


if __name__ == '__main__':
    import pprint

    sample_data = {
        "question_id": "K40ZY1kBHA64Ev-ch5bd"
    }

    pprint.pp(asyncio.run(questions_get_question_by_id(**sample_data)))
