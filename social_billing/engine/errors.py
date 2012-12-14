# -*- coding: utf-8 -*-
import tornado.locale


class BaseException(Exception):

    critical = 1

    def response(self):
        return {'error': {'error_code': self.code, 'error_msg': self.name,
                          'critical': self.critical}}


class SignatureError(BaseException):

    code = 10
    name = 'signature error'


class ItemFormatError(BaseException):

    code = 11
    name = 'item format error'


class UnknownItemError(BaseException):

    code = 20
    name = 'unknown item'


class InvalidCountError(BaseException):

    code = 21
    name = 'invalid count'


class CallbackError(BaseException):

    code = 1
    name = 'callback error'
