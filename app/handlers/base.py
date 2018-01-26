#--*-- coding: utf-8 --*--

import logging
from aiohttp import web
from app.utils.error_codes import ErrorCodes

class MMBaseApi(object):
    def __init__(self):
        pass

    async def reply_ok(self, resp):
        response = {"status": ErrorCodes.Ok.value, "message": "Ok", "data": {"result": resp if resp else []}}
        logging.info(response)
        return web.json_response(data = response)