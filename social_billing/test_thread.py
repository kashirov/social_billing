# -*- coding: utf8 -*-
from tests.base_test import BaseTest, TEST_PAYMENT_NAME
from social_billing.thread import BillingThread
from social_billing.vk.web.handler.base_handler import BaseHandler


class TestBillingThread(BaseTest):

    def test_init(self):
        thread = BillingThread(TEST_PAYMENT_NAME,
                               self.items, 'secretkey',
                               lambda x: True)
        self.eq(BaseHandler.payment.info.items, self.items)
        self.eq(BaseHandler.payment.db.name, 'payment_' + TEST_PAYMENT_NAME)

