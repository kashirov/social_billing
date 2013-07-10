# -*- coding: utf8 -*-
from tests.mm.mm_base_test import MMBaseTest


class MMPaymentTest(MMBaseTest):

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
        self.eq(self.payment.request(self.signed_args(mailiki_price=4)),
                self.price_error)
