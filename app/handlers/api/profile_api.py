#--*-- coding: utf-8 --*--

import json
import time
from aiohttp import web


async def my_profile(request):
    db = request.app['mongo_db']
    profile = db.moonmoonbird.profile.\
        find({"update_time": {"$lt": time.time()}}).\
        sort([('update_time', -1)]).limit(1)

    profile_data = []
    async for p in profile:
        profile_data.append(p)
    return web.json_response(data=profile_data)


def validate(fn):
    async def decorator(request, *args, **kwargs):
        ret = await fn(request, *args, **kwargs)
        return ret
    return decorator

@validate
async def post_profile(request):
    db = request.app['mongo_db'].moonmoonbird.profile
    profile = await request.json()
    print (profile)
    await db.insert(profile)
    return web.json_response(data='')