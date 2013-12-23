# -*- coding: utf-8 -*-
import hashlib
from social_billing.vk.engine.errors import SignatureError


class Signature(object):

    def __init__(self, key):
        self.key = key

    def string(self, *args):
        return ''.join(map(lambda x: str(x), args)) + self.key

    def md5(self, *args):
        return hashlib.md5(self.string(*args)).hexdigest()

    def check(self, sig, *args):
        return self.md5(*args) == sig

    def try_check(self, params):
        if not self.check(params, params.pop('sig', '')):
            raise SignatureError
