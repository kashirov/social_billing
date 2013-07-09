# -*- coding: utf8 -*-
from ztest import ZTest


class Engine(object):
    """
    Mock object for testing callback
    """

    def __init__(self):
        self.log = []

    def callback(self, receiver_id, name, count):
        self.log.append((receiver_id, name, count))
        return True


class BaseTest(ZTest):
    items = {
        'gems': {'prices': {10: 1, 20: 2},
                 'image': 'image_url'}
    }

    engine = Engine()

    def sign(self, args):
        args['sig'] = self.payment.signature.md5(args)
        return args

    def setUp(self):
        super(BaseTest, self).setUp()
        self.engine.log = []
