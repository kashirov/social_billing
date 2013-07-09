# -*- coding: utf-8 -*-
from urllib import urlencode

from tornado.web import Application

from social_billing.core import BillingCore
from tests.base_test import BaseTest
from social_billing.vk.engine.handler.vk_order import CHARGEABLE
from social_billing.vk.engine.payment import VKPayment, ORDER
from social_billing.vk.engine.payment import GET_ITEM


TEST_PREFIX = '_test'
GET_ITEM_TEST = GET_ITEM + TEST_PREFIX
ORDER_TEST = ORDER + TEST_PREFIX


TEST_PAYMENT_NAME = 'test'


class VKBaseTest(BaseTest):
    app = Application(debug=True)


    def callback(self, *args):
        return True

    def setUp(self):
        super(VKBaseTest, self).setUp()
        BillingCore.init('vk', TEST_PAYMENT_NAME, self.items, 'secretkey',
                         self.engine.callback)
        self.payment = VKPayment(TEST_PAYMENT_NAME, self.items, 'secretkey',
                               self.engine.callback)
        self.payment.order.collection.drop()


    def info_args(self, item='gems_10', ntype=GET_ITEM):
        return self.sign({'notification_type': ntype, 'item': item})

    def order_args(self, item='gems_10', ntype=ORDER):
        return self.sign({'notification_type': ntype, 'item': item,
                          'status': CHARGEABLE, 'order_id': 1,
                          'receiver_id': 'uid'})

    def error_callback(self, *a):
        return False
