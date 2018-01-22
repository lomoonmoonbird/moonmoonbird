#--*-- coding: utf-8 --*--

import json
import time
from collections import OrderedDict
from aiohttp import web
from app.utils.decorators import arg_parser
from app.handlers.base import MMBaseApi

"""
blog:Thread handler
"""
class Threads(MMBaseApi):
    """
    handler for manage threads
    """
    def __init__(self):
        pass

    # @classmethod
    @arg_parser(('title', str), ('content', str),
                ('tags', list), ('imgs', list),
                ('subtype', int), ('category', int))
    async def post_thread(self, request):
        """
        compose a new thread
        :param request:
        :return:
        """
        new_thread = OrderedDict([
            ('title',request.requestdata['title']),
            ('content',request.requestdata['content']),
            ('tags', request.requestdata['tags']),
            ('imgs', request.requestdata['imgs']),
            ('category', request.requestdata['category']),
            ('subtype', request.requestdata['subtype']),
            ('likes', 0),
            ('hates', 0),
            ('scanned', 0),
            ('create_time', time.time()),
            ('update_time', time.time())
        ])

        id = await request.app['mongo_db'].moonmoonbird.threads.insert(new_thread)

        return await self.reply_ok('')

    @arg_parser(('category', int),('subtype', int),
                ('page_type', int), ('create_time', float))
    async def get_threads(self, request):
        """
        get threads with create_time based pagination
        :param request:
        :return:
        """
        category = int(request.requestdata['category'])
        subtype = int(request.requestdata['subtype'])
        pagination_type = int(request.requestdata['page_type'])
        create_time = float(request.requestdata['create_time'])

        db = request.app['mongo_db'].moonmoonbird.threads
        query_condition = {"$lt": create_time} if pagination_type == 1 else {"$gt": create_time}
        # print (query_condition)
        threads = db.find({"create_time": query_condition}).sort([("create_time", -1)]).limit(20)

        ret = []
        async for thread in threads:
            thread['_id'] = str(thread['_id'])
            ret.append(thread)
        self.reply_ok(ret)

    @arg_parser(('11','22'), page=(int, 1), sortType=(int, 0))
    async def thread_detail(self, request):
        return web.json_response('')


