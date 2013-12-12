# -*- coding: utf8 -*-
from social_billing.core import BillingCore
from tests.base_test import BaseTest
from tests.vk.vk_base_test import TEST_PAYMENT_NAME


class ODBaseTest(BaseTest):

    def setUp(self):
        super(ODBaseTest, self).setUp()
        BillingCore.init('od', 'gems', TEST_PAYMENT_NAME, self.items,
                         'secretkey', self.engine.callback)
        self.payment = BillingCore.payment
        self.payment.order.collection.drop()

    def args(self, transaction_id=3751, amount=1):
        return dict(
            transaction_id=transaction_id, product_code=10,
            uid=104,
            amount=amount,
            other_price=10000,
            app_id=524632
        )

    def signed_args(self, **kw):
        return self.sign(self.args(**kw))


class ODPaymentTest(ODBaseTest):

    ok = {'status': 1}
    signature_error = {'status': 0, 'error_code': 700}
    price_error = {'status': 0, 'error_code': 703}

    def test_get_price(self):
        self.eq(self.payment.get_price(10), 1)
        self.eq(self.payment.get_price(20), 2)

    def test_buy(self):
        for _ in xrange(10):
            self.eq(self.payment.request(self.signed_args()), self.ok)
            self.eq(self.engine.log, [(104, 'gems', 10)])

        self.payment.request((self.signed_args(transaction_id=1)))
        self.eq(
            self.engine.log,
            [(104, 'gems', 10), (104, 'gems', 10)]
        )

    def test_signature_error(self):
        args = self.args()
        args['sig'] = 'errorsignature'
        self.eq(self.payment.request(args), self.signature_error)

    def test_price_error(self):
        self.eq(self.payment.request(self.signed_args(amount=4)),
                self.price_error)
