# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from tornado.web import url

from handlers.common import MetricsHandler
from handlers.common import SimpleHealthCheckHandler

from handlers.example import ExampleHandler1


ROUTES = [
    # 心跳检查
    url(r"/health.json", SimpleHealthCheckHandler),
    url(r"/prometheus", MetricsHandler),
    # 案例
    url(r"/example1", ExampleHandler1)
]
