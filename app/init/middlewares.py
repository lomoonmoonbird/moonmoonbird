#--*-- coding:utf-8 --*--

from app.utils.middlewares import handle_exception

def init_middlewares(app):
    app.middlewares.append(handle_exception)