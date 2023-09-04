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

    async def get_tags(self, db, tagids=[]):
        tags = db.moonmoonbird.tags.find({})
        real_tags = []
        async for t in tags:
            if str(t["_id"]) in tagids:
                real_tags.append(t['name'])
        return real_tags

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

    @arg_parser(('time', float), ('category_id', str))
    async def get_threads(self, request):
        """
        get threads with create_time based pagination
        :param request:
        :return:
        """
        category = str(request.requestdata['category_id'])
        create_time = float(request.requestdata['time'])

        db = request.app['mongo_db'].moonmoonbird.threads
        threads = db.find({"create_time": {"$lt": create_time}, "category": category}).sort([("create_time", -1)]).limit(12)

        ret = []
        async for thread in threads:
            thread['_id'] = str(thread['_id'])
            thread['tags'] = await self.get_tags(request.app['mongo_db'], thread['tags'])
            ret.append(thread)
        return await self.reply_ok(ret)


    async def get_all_threads(self, request):
        ret = request.app['mongo_db'].moonmoonbird.threads.find({})
        threads = []
        async for thread in ret:
            thread["id"] = str(thread['_id'])
            thread["tags"] = await self.get_tags(request.app['mongo_db'], thread['tags'])
            del thread["_id"]
            threads.append(thread)
        print (threads)
        return await self.reply_ok(threads)

    @arg_parser(('hash_url', str))
    async def thread_detail(self, request):
        one = await request.app['mongo_db'].moonmoonbird.threads.find_one({"hash_url": request.requestdata['hash_url']})
        one['id'] = str(one['_id'])
        one['tags'] = await self.get_tags(request.app['mongo_db'], one['tags'])
        del one["_id"]
        return await self.reply_ok(one)


    # @arg_parser(('iid', str))
    # async def






