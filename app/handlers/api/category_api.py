#--*-- coding: utf-8 --*--

"""
category for every type of content
"""

import time
from collections import OrderedDict
from aiohttp import web
from app.utils.decorators import arg_parser
from app.handlers.base import MMBaseApi
from bson import ObjectId

class Category(MMBaseApi):
    def __init__(self):
        pass

    @arg_parser(("name", str), ("desc", str), ("weight", int))
    async def post_category(self, request):
        new_tags = OrderedDict([
            # ('_id',request.requestdata['name']),
            ('name', request.requestdata['name']),
            ('desc',request.requestdata['desc']),
            ('weight', request.requestdata['weight']),
            ('create_time', time.time()),
            ('update_time', time.time())
        ])

        ret = await request.app['mongo_db'].moonmoonbird.category.update({"name": new_tags['name']},
                                                                     new_tags,
                                                                     upsert=True)
        return await self.reply_ok([])

    @arg_parser(("name", str), ("desc", str), ("weight", int),("id", str))
    async def update_category(self, request):

        new_tags = OrderedDict([
            # ('_id',request.requestdata['name']),
            ('name', request.requestdata['name']),
            ('desc',request.requestdata['desc']),
            ('weight', request.requestdata['weight']),
            ('update_time', time.time())
        ])

        ret = await request.app['mongo_db'].moonmoonbird.category.update({"_id": ObjectId(request.requestdata['id'])},
                                                                     new_tags)
        return await self.reply_ok([])

    @arg_parser(("id", str))
    async def delete_category(self, request):

        ret = await request.app['mongo_db'].moonmoonbird.category.remove({"_id": ObjectId(request.requestdata["id"])})
        return await self.reply_ok([])

    @arg_parser()
    async def get_category(self, request):
        """
        return tags sorted with weight
        :param request:
        :return:
        """
        tags = request.app['mongo_db'].moonmoonbird.category.find({}).sort([("weight", -1)])
        ret = []
        async for tag in tags:
            tag['id'] = str(tag['_id'])
            del tag['_id']
            ret.append(tag)

        return await self.reply_ok(ret)

