# -*- coding: utf8 -*-
from social_billing.base_test import BaseTest, TEST_PAYMENT_NAME
from social_billing.thread import BillingThread, main
from social_billing.web.handler.base_handler import BaseHandler


class TestBillingThread(BaseTest):

    def test_init(self):
        thread = BillingThread(TEST_PAYMENT_NAME,
                               {'gems': {5: 1, 10: 2}}, 'secretkey',
                               lambda x: True)
        self.eq(BaseHandler.payment.info.prices, {'gems': {5: 1, 10: 2}})
        self.eq(BaseHandler.payment.db.name, 'payment_' + TEST_PAYMENT_NAME)

