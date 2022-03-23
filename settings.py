# -*- coding: utf-8 -*-
import os
import logging
import threading
import jproperties


BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, 'config.properties')
_encoding = "utf-8"
_config_update_timeout = 0.05
_lock = threading.RLock()
_lock_ = threading.RLock()

app_settings = dict(
    debug=False,
    template_path=os.path.join(BASE_DIR, 'template'),
    static_path=os.path.join(BASE_DIR, 'static')
)


# -配置- #
def load_config(update_timeout=_config_update_timeout, lock=_lock):
    assert os.path.exists(CONFIG_PATH)
    with open(CONFIG_PATH, "rb") as f:
        lock.acquire(timeout=update_timeout)
        prop = jproperties.Properties()
        prop.load(f, encoding=_encoding)
    return prop


class Prop:
    _instance = None
    _init = False
    with _lock_:
        p = load_config()
    global_params = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Prop, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super(Prop, self).__init__()
        if not Prop._init:
            Prop.p = load_config()

    @staticmethod
    def __dict__(key):
        return Prop.get(key)

    @staticmethod
    def get(key, default=None):
        if key in Prop.p:
            return Prop.p[key].data
        return default

    def dump(self, **kwargs):
        with open(CONFIG_PATH, 'wb') as stream:
            for key, value in kwargs.items():
                self.p[key] = value
            self.p.store(stream, encoding=_encoding)


class LogFilter(logging.Filter):
    filter_prefix = ['/health', '/prometheus', '/docs']

    def filter(self, record):
        _path = record.args[1].split(' ')[1]
        for prefix in self.filter_prefix:
            if _path.startswith(prefix):
                return False
        return True


logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(processName)s-%(process)d]【Python服务】%(module)s.%(funcName)s : %(message)s")
settings = dict(debug=False)
