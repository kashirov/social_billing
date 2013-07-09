# -*- coding: utf-8 -*-
from tests.base_test import BaseTest, GET_ITEM_TEST, ORDER_TEST
from social_billing.vk.engine.errors import ItemFormatError, CallbackError, \
    SignatureError
from social_billing.vk.engine.handler.order import CHARGEABLE


class PaymentTest(BaseTest):

    def setUp(self):
        super(PaymentTest, self).setUp()

    def test_request_info(self):
        self.eq(self.payment.request(self.info_args()),
                self.payment.info('gems_10'))

    def test_request_info_test(self):
        self.eq(self.payment.request(self.info_args(ntype=GET_ITEM_TEST)),
                self.payment.info('gems_10'))

    def test_request_order(self):
        self.eq(self.payment.request(self.order_args()),
                self.payment.order(1, 'uid', 'gems_10', CHARGEABLE))

    def test_request_order_test(self):
        self.eq(self.payment.request(self.order_args(ntype=ORDER_TEST)),
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
