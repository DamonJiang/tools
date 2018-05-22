#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import random

def RandomCode(len = 10):
    return "".join(random.sample(
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",len))