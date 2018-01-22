# --*-- coding: utf-8 --*--

import functools


from app.utils.exceptions import RequestParamError

def arg_parser(*required_args, **optional_args):

    def decorator(fn, *args, **kwargs):
        @functools.wraps(fn)
        async def inner(self, handler, *args, **kwargs):
            query_args = {}
            handler.requestdata = {}
            if handler.match_info:
                for k, v in handler.match_info.items():
                    query_args[k] = v
            if handler.query:
                for k,v in handler.query.items():
                    query_args[k] = v

            if handler.has_body:
                for k,v in (await handler.json()).items():
                    query_args[k] = v
            def validate_type(key, key_type):
                try:
                    if not callable(key_type):
                        raise ValueError('data type must be callable')
                    v = query_args[key]
                    val = v if v is None else key_type(v)
                    handler.requestdata[key] = val
                    return True
                except:
                    msg = 'Argument {} must be type of {}'.format(key, key_type.__name__)
                    raise RequestParamError(msg)
            if required_args:
                for required_key_type in required_args:
                    if required_key_type[0] not in query_args:
                        msg = 'Miss argument {}'.format(required_key_type[0])
                        raise RequestParamError(msg)
                    else:
                        validate_type(required_key_type[0], required_key_type[1])

            if optional_args:
                for key, type_default in optional_args.items():
                    if key not in query_args:
                        query_args[key] = type_default[1]
                    else:
                        validate_type(key, type_default[0])
            resp = await fn(self, handler)
            return resp
        return inner
    return decorator

