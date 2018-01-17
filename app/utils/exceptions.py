from app.utils.error_codes import ErrorCodes


class AppException(Exception):
    def __init__(self, error_code, message=''):
        self.code = error_code
        self.message = message


class RequestParamError(AppException):
    def __init__(self, message):
        super(RequestParamError, self).__init__(ErrorCodes.BadRequest, message)


class ForbiddenError(AppException):
    def __init__(self, message):
        super(ForbiddenError, self).__init__(ErrorCodes.Forbidden, message)


class CacheHit(AppException):
    def __init__(self, data):
        self.code = ErrorCodes.Ok
        self.message = ''
        self.data = data