#--*-- coding: utf-8 --*--

from aiohttp import web

async def index(request):
    db = request.app['mongo_db']

    return web.json_response('')