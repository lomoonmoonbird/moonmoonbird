#--*-- coding: utf-8 --*--

from aiohttp import web
from app.utils.error_codes import ErrorCodes

class MMBaseApi(object):
    def __init__(self):
        pass

    def reply_ok(self, resp):
        response = {"status": ErrorCodes.Ok.value, "message": "Ok", "data": {"result": resp}}
        return web.json_response(data = response)