# -*- coding: utf-8 -*-
import hashlib


class Signature(object):

    def __init__(self, key):
        self.key = key

    def key_value(self, args):
        for kv in sorted(args.iteritems()):
            yield '%s=%s' % kv

    def string(self, args):
        return ''.join(self.key_value(args)) + self.key

    def md5(self, args):
        return hashlib.md5(self.string(args)).hexdigest()

    def check(self, params, sig):
        return self.md5(params) == sig
