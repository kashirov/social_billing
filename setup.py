#!/usr/bin/env python

from setuptools import setup

setup(name='social_billing',
      description='service for processing social payment',
      author='dsociative',
      author_email='admin@geektech.ru',
      packages=['social_billing', 'social_billing.web',
                'social_billing.web.handler',
                'social_billing.engine', 'social_billing.engine.handler'],
      package_data={'social_billing': ['translations/*.csv']},
      install_requires=['tornado', 'pymongo']
)
