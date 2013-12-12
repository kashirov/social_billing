# -*- coding: utf8 -*-
from social_billing.mm.engine.payment import MMPayment


class ODPayment(MMPayment):
    COUNT_FIELD = 'product_code'
    PRICE_FIELD = 'amount'
