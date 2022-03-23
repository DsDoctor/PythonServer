# -*- coding: utf-8 -*-
import json
import logging
from settings import Prop, load_config, _lock_


def update_config():
    try:
        prop = load_config(lock=_lock_)
        if not Prop.p or prop.properties != getattr(Prop.p, "properties"):
            Prop.p = prop
            logging.info(f"配置文件更新成功: {json.dumps(Prop.p.properties)}")

    except Exception as ex:
        logging.exception(ex)
        logging.error("配置文件更新失败")
