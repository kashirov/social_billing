# -*- coding: utf-8 -*-
from threading import Thread

from tornado.ioloop import IOLoop
from social_billing.core import BillingCore

from social_billing.web.app import application


class BillingThread(Thread):

    def __init__(self, social, name, prices, secret, callback, port=8888):
        super(BillingThread, self).__init__()
        BillingCore.init(social, name, prices, secret, callback)
        self.app = application
        self.port = port
        self.loop = IOLoop.instance()

    def run(self):
        self.app.listen(self.port)
        self.loop.start()

    def stop(self):
        self.loop.stop()


def main():
    from tests.vk.vk_base_test import TEST_PAYMENT_NAME

    def callback(self, *a):
        print a

    service = BillingThread(TEST_PAYMENT_NAME,
                            {'gems': {10: 1, 20: 2}}, 'secretkey', callback)
    service.run()
    print 'started'


if __name__ == '__main__':
    main()
