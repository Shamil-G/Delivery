from __init__ import app, log
import app_config as cfg
from util.utils import *
import view.routes
from db.conneсt import _pool


if __name__ == "__main__":
    if _pool:
        log.info(f"===> Main Delivery started on {cfg.host}:{cfg.port}, work_dir: {cfg.BASE}")
        app.run(host=cfg.host, port=cfg.port, debug=False)
    else:
        log.info(f"===> DB Postgre didn't start on {cfg.host}:{cfg.port}, work_dir: {cfg.BASE}")
