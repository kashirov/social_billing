# -*- coding: utf-8 -*-
import hashlib
from social_billing.vk.engine.errors import SignatureError


class Signature(object):

    def __init__(self, key, prefix='='):
        self.prefix = prefix
        self.key = key

    def key_value(self, args):
        for kv in sorted(args.iteritems()):
            yield self.prefix.join(map(str, kv))

    def string(self, args):
        return ''.join(self.key_value(args)) + self.key

    def md5(self, args):
        return hashlib.md5(self.string(args)).hexdigest()

    def check(self, params, sig):
        return self.md5(params) == sig

    def try_check(self, params):
        if not self.check(params, params.pop('sig', '')):
            raise SignatureError
