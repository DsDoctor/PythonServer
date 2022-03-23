# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import json

import prometheus_client
from prometheus_client.registry import CollectorRegistry

from handlers.metrics import MetricsRequestHandler
from handlers.metrics import MAIN_GET_LAST_EXCEPTION_DURATION_SECOND
from tornado.log import app_log as logger


class SimpleHealthCheckHandler(MetricsRequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        start_time = time.time()
        try:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(json.dumps({'status': 'UP'}))
        except Exception as ex:
            message = f'error when deal the get request. exception: {ex}'
            logger.error(message)
            self.write(message)
            MAIN_GET_LAST_EXCEPTION_DURATION_SECOND.set(time.time() - start_time)


class MetricsHandler(MetricsRequestHandler):
    registry: CollectorRegistry

    def data_received(self, chunk):
        pass

    def initialize(self, registry=prometheus_client.REGISTRY):
        self.registry = registry

    def get(self):
        encoder, content_type = prometheus_client.exposition.choose_encoder(self.request.headers.get('Accept'))
        self.set_header('Content-Type', content_type)
        self.write(encoder(self.registry))
