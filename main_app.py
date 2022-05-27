from __init__ import app, log
import app_config as cfg
from util.utils import *
import view.routes

if __name__ == "__main__":
    log.info(f"===> Main Delivery started on {cfg.host}:{cfg.port}, work_dir: {cfg.BASE}")
    app.run(host=cfg.host, port=cfg.port, debug=False)
