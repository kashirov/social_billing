# -*- coding: utf-8 -*-
import tornado.locale


class BaseException(Exception):

    @property
    def msg(self):
        locale = tornado.locale.get('ru_RU')
        return locale.translate(self.name)


class ItemFormatError(BaseException):

    code = 10
    name = 'item format error'


class UnknownItemError(BaseException):

    code = 11
    name = 'unknown item'


class InvalidCountError(BaseException):

    code = 12
    name = 'invalid count'
