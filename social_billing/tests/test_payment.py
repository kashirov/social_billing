# -*- coding: utf-8 -*-
from social_billing.base_test import BaseTest
from social_billing.errors import ItemFormatError, UnknownItemError,\
    InvalidCountError, CallbackError, SignatureError
from social_billing.payment import Payment
from social_billing.order import CHARGEABLE


class PaymentTest(BaseTest):

    def setUp(self):
        super(PaymentTest, self).setUp()

    def test_request_info(self):
        self.eq(self.payment.request(self.info_args()),
                self.payment.info('gems_10'))

    def test_request_order(self):
        self.eq(self.payment.request(self.order_args()),
                self.payment.order(1, 'uid', 'gems_10', CHARGEABLE))

    def test_request_error_order(self):
        self.eq(self.payment.request(self.order_args('gems10')),
                ItemFormatError().response())

    def test_request_error_callback(self):
        self.payment.order.callback = self.error_callback
        self.eq(self.payment.request(self.order_args('gems_10')),
                CallbackError().response())

    def test_request_error_sig(self):
        args = self.order_args('gems_10')
        args['sig'] = 'error'
        self.eq(self.payment.request(args),
                SignatureError().response())
