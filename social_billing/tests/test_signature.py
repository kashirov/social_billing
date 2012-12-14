# -*- coding: utf-8 -*-
from hashlib import md5

from social_billing.base_test import BaseTest
from social_billing.signature import Signature


class SignatureTest(BaseTest):

    def setUp(self):
        self.signature = Signature('secretkey')
        self.params = {'c': 'a', 'b': 'v', 'a': 'z'}

    def test_string(self):
        self.eq(self.signature.string(self.params),
                'a=zb=vc=a' + self.signature.key)

    def test_md5(self):
        self.eq(self.signature.md5(self.params),
                md5(self.signature.string(self.params)).hexdigest())

    def test_check(self):
        self.true(self.signature.check(self.params,
                                       self.signature.md5(self.params)))
        self.false(self.signature.check(self.params, 'qwe'))
