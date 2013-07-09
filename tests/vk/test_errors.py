# -*- coding: utf-8 -*-
from tests.vk.vk_base_test import VKBaseTest
from social_billing.vk.engine.errors import CallbackError, InvalidCountError,\
    ItemFormatError, UnknownItemError


class ErorrsTest(VKBaseTest):

    def test_item_format(self):
        error = ItemFormatError()
        self.eq(error.code, 11)
        self.eq(error.name, u'item format error')

    def test_unknown_item(self):
        error = UnknownItemError()
        self.eq(error.code, 20)
        self.eq(error.name, u'unknown item')

    def test_invalid_count(self):
        error = InvalidCountError()
        self.eq(error.code, 21)
        self.eq(error.name, u'invalid count')

    def test_callback_error(self):
        error = CallbackError()
        self.eq(error.code, 1)
        self.eq(error.name, u'callback error')
