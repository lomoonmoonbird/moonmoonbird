#--*-- coding: utf-8 --*--

import pathlib

from app.handlers.api.index_api import Index
from app.handlers.api.thread_api import Threads
from app.handlers.api.tags_api import Tags
from app.handlers.api.category_api import Category

PROJECT_ROOT = pathlib.Path(__file__).parent


def init_routers(app):
    prefix = '/api'
    t = Threads()
    index = Index()
    tag = Tags()
    category = Category()

    #index
    app.router.add_get('/', index.index)

    #tags
    app.router.add_get(prefix + '/tags/list', tag.get_tags)
    app.router.add_post(prefix + '/tags/post', tag.post_tag)
    app.router.add_put(prefix + '/tags/update', tag.update_tag)
    app.router.add_delete(prefix + '/tags/delete', tag.delete_tag)

    #categoty
    app.router.add_post(prefix + '/category/post', category.post_category)
    app.router.add_get(prefix + '/category/list', category.get_category)
    app.router.add_put(prefix + '/category/update', category.update_category)
    app.router.add_delete(prefix + '/category/delete', category.delete_category)
    #threads
    app.router.add_post('/api/threads/post', t.post_thread)
    app.router.add_get('/api/threads/detail', t.thread_detail)
    app.router.add_get('/api/threads/all', t.get_all_threads    )
    app.router.add_put('/api/threads/update', t.update_thread)
    app.router.add_get('/api/threads/page', t.get_threads)

    # app.router.add_get('/api/blog/threads', get_threads)
    # app.router.add_get('/api/blog/thread', thread_detail)


    # app.router.add_get('/poll/{question_id}', poll, name='poll')
    # app.router.add_get('/poll/{question_id}/results',
    #                    results, name='results')
    # app.router.add_post('/poll/{question_id}/vote', vote, name='vote')

