from __init__ import app, log
import app_config as cfg
from util.utils import *
from flask import make_response, request, send_from_directory, render_template
import requests
import os
import view.routes

if __name__ == "__main__":
    log.info(f"===> Main Receipt started on {cfg.host}:{cfg.port}, work_dir: {cfg.BASE}")
    app.run(host=cfg.host, port=cfg.port, debug=False)
