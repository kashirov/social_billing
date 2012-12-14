# -*- coding: utf-8 -*-
from tornado.httpserver import HTTPRequest
from tornado.web import Application
from ztest import ZTest

from social_billing.handler.base_handler import BaseHandler
from social_billing.payment import ORDER, GET_ITEM, Payment
from social_billing.order import CHARGEABLE
from social_billing.payment import ORDER


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


class Engine(object):
    '''
    Mock object for testing callback
    '''

    def __init__(self):
        self.log = []

    def callback(self, receiver_id, name, count):
        self.log.append((receiver_id, name, count))
        return True


class BaseTest(ZTest):

    app = Application(debug=True)
    prices = {'gems': {10: 1, 20: 2}}

    def callback(self, *args):
        return True

    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        BaseHandler.init(self.prices, 'secretkey', self.callback)

    def setUp(self):
        self.engine = Engine()
        self.payment = Payment(self.prices, 'secretkey',
                               self.engine.callback)
        self.payment.collection.drop()

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

    def sign(self, args):
        args['sig'] = self.payment.signature.md5(args)
        return args

    def info_args(self, item='gems_10'):
        return self.sign({'notification_type': GET_ITEM, 'item': item})

    def order_args(self, item='gems_10'):
        return self.sign({'notification_type': ORDER, 'item': item,
                          'status': CHARGEABLE, 'order_id': 1,
                          'receiver_id': 'uid'})

    def error_callback(self, *a):
        return False
