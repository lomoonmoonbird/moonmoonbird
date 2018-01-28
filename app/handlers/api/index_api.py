#--*-- coding: utf-8 --*--

from aiohttp import web
from app.handlers.base import MMBaseApi

class Index(MMBaseApi):

    def __init__(self):
        pass

    async def index(self, request):
        db = request.app['mongo_db']
        threads = db.moonmoonbird.threads.find({}).limit(12)
        ret = []
        async for t in  threads:
            t['_id'] = str(t['_id'])
            ret.append(t)

        return await self.reply_ok(ret)