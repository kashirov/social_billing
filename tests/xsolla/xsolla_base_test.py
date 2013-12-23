# -*- coding: utf-8 -*-
from urllib import urlencode

from tornado.web import Application

from social_billing.core import BillingCore
from social_billing.xsolla.engine.payment import XsollaPayment, CHECK, PAY
from tests.base_test import BaseTest


TEST_PAYMENT_NAME = 'test'


class XsollaBaseTest(BaseTest):
    app = Application(debug=True)


    def callback(self, *args):
        return True

    def setUp(self):
        super(XsollaBaseTest, self).setUp()
        BillingCore.init(
            'vk', 'gems', TEST_PAYMENT_NAME, self.items, 'secretkey',
            self.engine.callback
        )
        self.payment = XsollaPayment(TEST_PAYMENT_NAME, self.items, 'secretkey',
                               self.engine.callback)
        self.payment.order.collection.drop()

    def sign(self, *args):
        return self.payment.signature.md5(*args)

    def check_args(self, **kw):
        kw['md5'] = self.sign(kw.get('command'), kw.get('v1'))
        return kw

    def order_args(self, **kw):
        kw['md5'] = self.sign(kw.get('command'), kw.get('v1'), kw.get('id'))
        return kw

    def error_callback(self, *a):
        return False