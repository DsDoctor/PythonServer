# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tornado.web import RequestHandler
from tornado.log import access_log
from prometheus_client import Summary, Counter, Gauge

""" All the metrics should be defined in here, so that we could manage info easily.
Reference URL - https://github.com/prometheus/client_python
"""
# Create a COUNTER metric to the total amount of metrics.
EXCEPTION_COUNT = Counter('exception', 'Amount of exception')

# Create a GAUGE metric to track the time spent of last exception
LAST_EXCEPTION_DURATION_SECOND = Gauge('last_exception_duration_second',
                                       'The time spent of the last exception call',
                                       ['method', 'exception'])

MAIN_GET_LAST_EXCEPTION_DURATION_SECOND = \
    LAST_EXCEPTION_DURATION_SECOND.labels('SimpleHealthCheckHandler.GET', 'Exception')
EXCEPTION_GET_LAST_EXCEPTION_DURATION_SECOND = \
    LAST_EXCEPTION_DURATION_SECOND.labels('ExceptionHandler.GET', 'ValueError')

# Create a SUMMARY metric to track time spent and requests made.
COMMON_REQUEST_TIME = Summary('http_server_requests_seconds', 'Time spent processing request',
                              ['method', 'uri', 'status'])


class MetricsRequestHandler(RequestHandler):

    def data_received(self, chunk):
        """Implement this method to handle streamed request data.

                Requires the `.stream_request_body` decorator.
                """
        raise NotImplementedError()

    def write_error(self, status_code, **kwargs):
        EXCEPTION_COUNT.inc(1)
        super().write_error(status_code, **kwargs)

    def send_error(self, status_code=500, **kwargs):
        EXCEPTION_COUNT.inc(1)
        super().send_error(status_code, **kwargs)

    def on_finish(self):
        try:
            request_time = COMMON_REQUEST_TIME.labels(self.request.method, self.request.path, self.get_status())
            request_time.observe(self.request.request_time())
        except Exception as e:
            access_log.warn("Fail to record the metric of request - " + str(Exception) + str(e))
            EXCEPTION_COUNT.inc(1)
