# -*- coding: utf-8 -*-
from social_billing.xsolla.engine.response import Response


class BaseException(Exception, Response):

    pass


class SignatureError(BaseException):

    code = 3
    comment = 'signature error'


class ItemFormatError(BaseException):

    code = 4
    name = 'item format error'


class UnknownItemError(BaseException):

    code = 4
    name = 'unknown item'


class InvalidCountError(BaseException):

    code = 4
    name = 'invalid count'


class CallbackError(BaseException):

    code = 5
    name = 'callback error'
