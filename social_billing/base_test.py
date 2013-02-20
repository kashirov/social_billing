# -*- coding: utf-8 -*-
from urllib import urlencode
from tornado.httpserver import HTTPRequest
from tornado.web import Application
from ztest import ZTest

from social_billing.engine.handler.order import CHARGEABLE
from social_billing.engine.payment import Payment, ORDER
from social_billing.web.handler.base_handler import BaseHandler
from social_billing.engine.payment import GET_ITEM


TEST_PREFIX = '_test'
GET_ITEM_TEST = GET_ITEM + TEST_PREFIX
ORDER_TEST = ORDER + TEST_PREFIX


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
        self.request.body = urlencode(args)


class Engine(object):
    """
    Mock object for testing callback
    """

    def __init__(self):
        self.log = []

    def callback(self, receiver_id, name, count):
        self.log.append((receiver_id, name, count))
        return True


TEST_PAYMENT_NAME = 'test'


class BaseTest(ZTest):
    app = Application(debug=True)
    prices = {'gems': {10: 1, 20: 2}}

    def callback(self, *args):
        return True

    def setUp(self):
        BaseHandler.init(TEST_PAYMENT_NAME, self.prices, 'secretkey',
                         self.callback)
        self.engine = Engine()
        self.payment = Payment(TEST_PAYMENT_NAME, self.prices, 'secretkey',
                               self.engine.callback)
        self.payment.collection.drop()

    def proxy(self, data):
        return data

    def override(self, handler):
        handler.post = MethodHook(handler, handler.post)
        handler.finish = self.proxy
        return handler

    def request(self, method='GET', url=''):
        return HTTPRequest(method, url)

    def fake(self, handler_cls, method='GET'):
        if not FakeMixin in handler_cls.__bases__:
            handler_cls.__bases__ += (FakeMixin,)
        return self.override(handler_cls(self.app,
                                         self.request(method)))

    def sign(self, args):
        args['sig'] = self.payment.signature.md5(args)
        return args

    def info_args(self, item='gems_10', ntype=GET_ITEM):
        return self.sign({'notification_type': ntype, 'item': item})

    def order_args(self, item='gems_10', ntype=ORDER):
        return self.sign({'notification_type': ntype, 'item': item,
                          'status': CHARGEABLE, 'order_id': 1,
                          'receiver_id': 'uid'})

    def error_callback(self, *a):
        return False
