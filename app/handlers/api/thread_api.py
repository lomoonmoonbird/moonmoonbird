#--*-- coding: utf-8 --*--

import json
import time
from bson import ObjectId
from collections import OrderedDict
from aiohttp import web
from app.utils.decorators import arg_parser
from app.handlers.base import MMBaseApi
from hashids import Hashids

"""
blog:Thread handler
"""
class Threads(MMBaseApi):
    """
    handler for manage threads
    """
    def __init__(self):
        pass

    @arg_parser(('title', str),
                ('html_content', str),('tags', list),('desc', str),
                ('category', str), ('thumbnail', str))
    async def post_thread(self, request):
        """
        compose a new thread
        :param request:
        :return:
        """
        ret = await request.app['mongo_db'].moonmoonbird.counter.find_and_modify(query={"_id": "thread_id"},
                                          update={'$inc': {"num": 1}},
                                          # fields={'name': 1},
                                          upsert=True,
                                          new=True  ,
                                          full_response=True,
                                          manipulate=True)

        id = ret['value']['num']
        new_thread = OrderedDict([
            ('title',request.requestdata['title']),
            # ('markdown_content',request.requestdata['markdown_content']),
            ('desc', request.requestdata['desc']),
            ('html_content' ,request.requestdata['html_content']),
            ('tags', request.requestdata['tags']),
            ('thumbnail', request.requestdata['thumbnail']),
            ('category', request.requestdata['category']),
            ('hash_url', Hashids(salt=request.app['config']['hashid']['salt'],
                                 min_length=request.app['config']['hashid']['len']).encode(id)),
            # ('subtype', request.requestdata['subtype']),
            ('likes', 0),
            ('hates', 0),
            ('scanned', 0),
            ('uv', 0),
            ('pv', 0),
            ('create_time', time.time()),
            ('update_time', time.time())
        ])


        id = await request.app['mongo_db'].moonmoonbird.threads.insert(new_thread)

        return await self.reply_ok('')

    @arg_parser(('title', str),("id", str),
                ('html_content', str), ('tags', list), ('desc', str),
                ('category', str), ('thumbnail', str))
    async def update_thread(self, request):
        """
        update thread
        :param request:
        :return:
        """
        new_thread = OrderedDict([
            ('title', request.requestdata['title']),
            ('html_content', request.requestdata['html_content']),
            ('tags', request.requestdata['tags']),
            ('thumbnail', request.requestdata['thumbnail']),
            ('category', request.requestdata['category']),
            ('update_time', time.time())
        ])

        collection = request.app['mongo_db'].moonmoonbird.threads
        await collection.update({"_id": ObjectId(request.requestdata['id'])},
                                {"$set": new_thread})
        return await self.reply_ok([])

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


    async def get_all_threads(self, request):
        ret = request.app['mongo_db'].moonmoonbird.threads.find({})
        threads = []
        async for thread in ret:
            thread["id"] = str(thread['_id'])
            del thread["_id"]
            threads.append(thread)
        print (threads)
        return await self.reply_ok(threads)

    @arg_parser(('hash_url', str))
    async def thread_detail(self, request):
        one = await request.app['mongo_db'].moonmoonbird.threads.find_one({"hash_url": request.requestdata['hash_url']})
        one['id'] = str(one['_id'])
        del one["_id"]
        return await self.reply_ok(one)


    @arg_parser(('iid', str))
    async def 






