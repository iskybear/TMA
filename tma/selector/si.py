# coding: utf-8

from tma.utils import OrderedAttrDict


class ShareIndicators(object):
    def __init__(self, code):
        self.code = code
        self.indicators = OrderedAttrDict(code=code)




