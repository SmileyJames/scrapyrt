# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import collections


class MetaSpider(Spider):
    """Copy-paste from scrapy tests."""

    name = 'meta'

    def __init__(self, *args, **kwargs):
        super(MetaSpider, self).__init__(*args, **kwargs)
        self.meta = {}

    def closed(self, reason):
        self.meta['close_reason'] = reason


class SingleRequestSpider(MetaSpider):
    """Copy-paste from scrapy tests."""
    seed = None
    callback_func = None
    errback_func = None
    name = 'single_request'

    def start_requests(self):
        if isinstance(self.seed, Request):
            yield self.seed.replace(callback=self.parse, errback=self.on_error)
        else:
            yield Request(self.seed, callback=self.parse, errback=self.on_error)

    def parse(self, response):
        self.meta.setdefault('responses', []).append(response)
        if isinstance(self.callback_func, collections.Callable):
            return self.callback_func(response)
        if 'next' in response.meta:
            return response.meta['next']

    def on_error(self, failure):
        self.meta['failure'] = failure
        if isinstance(self.errback_func, collections.Callable):
            return self.errback_func(failure)
