# -*- coding: utf8 -*-
from social_billing.core import BillingCore
from tests.vk.vk_base_test import VKBaseTest, TEST_PAYMENT_NAME
from social_billing.thread import BillingThread


class TestBillingThread(VKBaseTest):

    def test_init(self):
        thread = BillingThread('vk', 'gems', TEST_PAYMENT_NAME,
                               self.items, 'secretkey',
                               lambda x: True)
        self.eq(BillingCore.payment.info.items, self.items)
        self.eq(BillingCore.payment.order.db.name,
                'payment_' + TEST_PAYMENT_NAME)

