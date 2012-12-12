# -*- coding: utf-8 -*-
from tornado.httpserver import HTTPRequest
from tornado.web import Application
from ztest import ZTest

from social_billing.handler.base_handler import BaseHandler


class MethodHook(object):

    def __init__(self, handler, method):
        self.handler = handler
        self.method = method

    def __call__(self, args):
        self.handler.set_args(args)
        return self.method()


class FakeMixin(object):

    def process_args(self, args):
        for key, value in args.iteritems():
            yield key, [value]

    def set_args(self, args):
        self.request.arguments = dict(self.process_args(args))


class BaseTest(ZTest):

    app = Application(debug=True)

    def callback(self, *args):
        pass

    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        BaseHandler.init({'gems': {10: 1, 20: 2}}, self.callback)

    def proxy(self, data):
        return data

    def override(self, handler):
        handler.post = MethodHook(handler, handler.post)
        handler.finish = self.proxy
        return handler

    def fake(self, handler_cls, method='GET'):
        if not FakeMixin in handler_cls.__bases__:
            handler_cls.__bases__ += (FakeMixin,)
        return self.override(handler_cls(self.app,
                                         HTTPRequest(method, '')))
