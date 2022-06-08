from main_app import app, log
import app_config as cfg
from util.i18n import i18n
from flask import send_from_directory, session, redirect, url_for, request
import psutil
import os


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    if cfg.debug_level > 0:
        log.debug(f"file for upload: {cfg.REPORTS_PATH}/{filename}")
    return send_from_directory(cfg.REPORTS_PATH, filename)


@app.route('/language/<string:lang>')
def set_language(lang):
    if cfg.debug_level > 3:
        log.debug(f"Set Language: {lang}, предыдущий язык: {session['language']}")
    session['language'] = lang
    # Получим предыдущую страницу, чтобы на неё вернуться
    current_page = request.referrer
    if cfg.debug_level > 3:
        log.debug(f"Set Language: {current_page}")
    if current_page is not None:
        return redirect(current_page)
    else:
        return redirect(url_for('view_index'))


@app.context_processor
def utility_processor():
    if cfg.debug_level > 3:
        log.debug(f"Context processor: {get_i18n_value('APP_NAME')}")
    return dict(res_value=get_i18n_value)


def get_i18n_value(res_name):
    try:
        lang = session['language']
    except KeyError:
        lang = 'ru'
    finally:
        session['language'] = lang
    if cfg.debug_level > 4:
        log.debug(f'Get i18N value: {lang} : {res_name}')
    return_value = i18n.get_resource(lang, res_name)
    if cfg.debug_level > 3:
        log.debug(f'Get i18N request value: {return_value}')
    return return_value


def print_memory(fn):
    def wrapper(*args, **kwargs):
        pr = psutil.Process(os.getpid())
        pr.memory_info()
        try:
            start_mem = pr.memory_info()
            # log.debug(f'===============> Start {fn.__name__.upper()}: {start_mem}')
            return fn(*args, **kwargs)
        finally:
            finish_mem = pr.memory_info()
            # log.debug(f'-----memory----> Stop  {fn.__name__.upper()}: {finish_mem}')
            log.debug(f'-----memory----> DEBUG {fn.__name__.upper()}: '
                      f'rss({finish_mem.rss-start_mem.rss}), '
                      f'vms({finish_mem.vms-start_mem.vms})'
                      #f'num_page_faults({finish_mem.num_page_faults-start_mem.num_page_faults}), '
                      #f'peak_wset({finish_mem.peak_wset-start_mem.peak_wset}), '
                      #f'wset({finish_mem.wset-start_mem.wset}), '
                      #f'peak_paged_pool({finish_mem.peak_paged_pool-start_mem.peak_paged_pool}), '
                      #f'paged_pool({finish_mem.paged_pool-start_mem.paged_pool}), '
                      #f'peak_nonpaged_pool({finish_mem.peak_nonpaged_pool-start_mem.peak_nonpaged_pool}), '
                      #f'nonpaged_pool({finish_mem.nonpaged_pool-start_mem.nonpaged_pool}), '
                      #f'pagefile({finish_mem.pagefile-start_mem.pagefile}), '
                      #f'peak_pagefile({finish_mem.peak_pagefile-start_mem.peak_pagefile}), '
                      #f'private({finish_mem.private-start_mem.private}) '
                      )
    return wrapper
