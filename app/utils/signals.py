# --*-- coding: utf-8 --*--

async def response_header(request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'
