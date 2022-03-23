# -*- coding: utf-8 -*-
from handlers.metrics import MetricsRequestHandler

from tornado.httpclient import AsyncHTTPClient


class ExampleHandler1(MetricsRequestHandler):
    def data_received(self, chunk):
        pass

    async def get(self):
        """
        异步http请求案例
        """
        client = AsyncHTTPClient()
        resp = await client.fetch('https://fanyi.baidu.com/?aldtype=16047#zh/en/python%E5%8D%8F%E7%A8%8B%E6%9C%8D%E5%8A%A1')
        self.write(resp.body)
