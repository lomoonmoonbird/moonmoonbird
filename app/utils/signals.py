# --*-- coding: utf-8 --*--

async def response_header(request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Client-Header, Accept-Encoding, Accept, Accept-Language, Access-Control-Request-Headers, Access-Control-Request-Method, content-type, authorization, content-length, x-requested-with, accept, origin'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Request-Headers'] = "Content-Type, content-type, X-Client-Header"
    response.headers['Server'] = "moonmoonbird"
    # response.headers['Access-Control-Request-Method'] = "POST, GET, PUT, OPTIONS"
    # response.headers['Access-Control-Allow-Methods'] = '*'
