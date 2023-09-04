#--*-- coding:utf-8 --*--

from aiohttp.web import middleware
from aiohttp import web
from app.utils.exceptions import RequestParamError
import logging

@middleware
async def handle_exception(request, handler):
    logging.info('jinpeng')
    if request.method == "OPTIONS":
        return web.json_response('')
    try:
        resp = await handler(request)
        logging.info(resp)
        return resp
    except RequestParamError as rp:
        logging.info(rp.message)
        return web.json_response(rp.message)


# async def handle_exception(app, handler):
#     print ('app', app)
#     async def handle(request):
#         return await handler(request)
#     return handle




