#--*-- coding: utf-8 --*--

"""
tags for every type of content
"""

import time
from collections import OrderedDict
from aiohttp import web
from app.utils.decorators import arg_parser
from app.handlers.base import MMBaseApi

class Tags(MMBaseApi):
    def __init__(self):
        pass

    @arg_parser(("name", str), ("desc", str), ("weight", int))
    async def post_tag(self, request):
        new_tags = OrderedDict([
            ('_id',request.requestdata['name']),
            ('desc',request.requestdata['desc']),
            ('weight', request.requestdata['weight']),
            ('create_time', time.time()),
            ('update_time', time.time())
        ])

        ret = await request.app['mongo_db'].moonmoonbird.tags.update({"_id": new_tags['_id']},
                                                                     new_tags,
                                                                     upsert=True)
        return self.reply_ok([])

    @arg_parser()
    async def get_tags(self, request):
        """
        return tags sorted with weight
        :param request:
        :return:
        """
        tags = request.app['mongo_db'].moonmoonbird.tags.find({}).sort([("weight", -1)])
        ret = []
        async for tag in tags:
            ret.append(tag)

        return self.reply_ok(ret)

