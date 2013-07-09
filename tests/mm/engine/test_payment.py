# -*- coding: utf8 -*-
from tests.mm.mm_base_test import MMBaseTest


class MMPaymentTest(MMBaseTest):

    ok = {'status': 1}
    signature_error = {'status': 0, 'error_code': 700}

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
