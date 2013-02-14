# -*- coding: utf-8 -*-
from social_billing.base_test import BaseTest
from social_billing.engine.errors import InvalidCountError, UnknownItemError, \
    ItemFormatError
from social_billing.web.handler.index_handler import IndexHandler, GET_ITEM
from social_billing.engine.handler.order import CHARGEABLE


class IndexTest(BaseTest):
    def setUp(self):
        super(IndexTest, self).setUp()
        self.handler = self.fake(IndexHandler)
        self.payment = self.handler.payment

    def test_args_empty_arg(self):
        self.handler.request = self.request(url='?item_id=&item_image_url=')
        self.eq(self.handler.args(), {'item_id': '', 'item_image_url': ''})

    def test_post_get_info(self):
        self.eq(self.handler.post(self.info_args('gems_20')),
                self.payment.info('gems_20'))

    def test_post_get_info_test(self):
        self.eq(self.handler.post(self.info_args('gems_20',
                                                 ntype=GET_ITEM + '_test')),
                self.payment.info('gems_20'))

    def test_post_order(self):
        self.eq(self.handler.post(self.order_args()),
                self.payment.order('1', 'uid', 'gems_10', CHARGEABLE))

    def test_errors(self):
        for error, item in [(ItemFormatError(), 'gems_no'),
                            (UnknownItemError(), 'coins_10'),
                            (InvalidCountError(), 'gems_11')]:
            self.eq(self.handler.post(self.info_args(item=item)),
                    error.response())
