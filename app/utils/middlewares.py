#--*-- coding:utf-8 --*--

from aiohttp.web import middleware
from aiohttp import web
from app.utils.exceptions import RequestParamError

@middleware
async def handle_exception(request, handler):
    try:
        resp = await handler(request)
        print ('@@@@@')
    except RequestParamError as rp:
        print (handler)
        return web.json_response('a')





