# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import tornado.web
from tornado.log import access_log
from tornado.ioloop import IOLoop
from tornado_swagger.setup import setup_swagger
from apscheduler.schedulers.background import BackgroundScheduler

from handlers import ROUTES
from scheduler.config import update_config
from scheduler import ScheduleMethod

from settings import Prop, LogFilter, app_settings


class Application(tornado.web.Application):
    def __init__(self, _routes, **kwargs):
        setup_swagger(_routes, title='Python服务', swagger_url='/doc', description='', api_version='0.0.1',
                      api_base_url='/' if Prop.get('env') != 'local' else '')
        super().__init__(_routes, **kwargs)
        self.scheduler = self.load_schedule()
        self.scheduler.start()

    @staticmethod
    def load_schedule():
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_config, ScheduleMethod.INTERVAL, seconds=30, name='配置更新')
        return scheduler


def make_app():
    logging.basicConfig(level=logging.INFO)
    _app = Application(ROUTES, **app_settings)
    access_log.addFilter(LogFilter())
    return _app


if __name__ == "__main__":
    app = make_app()
    app.listen(7777)

    logging.info('超高性能Python服务已启动 - port: 7777')
    IOLoop.current().start()
