# -*- coding: utf8 -*-
from social_billing.mm.engine.payment import MMPayment
from tests.base_test import BaseTest
from tests.vk.vk_base_test import TEST_PAYMENT_NAME


class MMBaseTest(BaseTest):

    def setUp(self):
        super(MMBaseTest, self).setUp()
        self.secret = 'secretkey'
        self.payment = MMPayment(TEST_PAYMENT_NAME, self.items, 'secretkey',
                                 self.engine.callback)
        self.payment.order.collection.drop()

    def args(self, transaction_id=3751):
        return dict(
            transaction_id=transaction_id, service_id=10,
            uid=104,
            mailiki_price=10, other_price=10000,
            profit=5000,
            app_id=524632
        )

    def signed_args(self, **kw):
        return self.sign(self.args(**kw))