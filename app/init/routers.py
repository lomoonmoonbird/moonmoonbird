#--*-- coding: utf-8 --*--

import pathlib

from app.handlers.api.index_api import Index
from app.handlers.api.thread_api import Threads

PROJECT_ROOT = pathlib.Path(__file__).parent


def init_routers(app):
    t = Threads()
    index = Index()
    # print (app['mongo_db'])
    #index
    app.router.add_get('/', index.index)

    #threads
    app.router.add_post('/api/blog/threads', t.post_thread)
    # app.router.add_get('/api/blog/threads', get_threads)
    # app.router.add_get('/api/blog/thread', thread_detail)


    # app.router.add_get('/poll/{question_id}', poll, name='poll')
    # app.router.add_get('/poll/{question_id}/results',
    #                    results, name='results')
    # app.router.add_post('/poll/{question_id}/vote', vote, name='vote')

