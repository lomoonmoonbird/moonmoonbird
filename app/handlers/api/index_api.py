#--*-- coding: utf-8 --*--

from aiohttp import web
from app.handlers.base import MMBaseApi

class Index(MMBaseApi):

    def __init__(self):
        pass

    async def get_tags(self, db, tagids=[]):
        tags = db.moonmoonbird.tags.find({})
        real_tags = []
        async for t in tags:
            if str(t["_id"]) in tagids:
                real_tags.append(t['name'])
        return real_tags

    async def index(self, request):
        db = request.app['mongo_db']
        threads = db.moonmoonbird.threads.find({}).limit(12)
        ret = []
        async for t in  threads:
            t['_id'] = str(t['_id'])
            t['tags'] = await self.get_tags(db, t['tags'])
            ret.append(t)

        return await self.reply_ok(ret)