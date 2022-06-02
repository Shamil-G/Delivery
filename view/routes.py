from flask import render_template, session, redirect, url_for, make_response, request
from util.utils import *
from main_app import app, log
import app_config as cfg
from model.get_status import get_status
import requests
import json
from model.yandex import *


# @app.route('/status_mykhat', methods=['POST', 'GET'])
# def view_status_mykhat():
#     # result = session['result']
#     # print(f"===> VIEW STATUS myKHAT. PAYMENTS. url: {cfg.myKHAT_host} : {result}")
#     # if 'iscash' in result and result['iscash']==False:
#     #     return redirect('new_order_mykhat')
#     # else:
#     return redirect(cfg.myKHAT_host)


@app.route('/status_yandex', methods=['POST', 'GET'])
def view_status_yandex():
    if 'result' not in session:
        print(f'-----> Yandex. Redirect to view_index ')
        return redirect(url_for('view_index'))
    new_url = request_yandex()
    print(f'-----> Yandex. Redirect to: {new_url} ')
    return redirect(new_url)


@app.route('/delivery/<string:iin>/<string:num_order>', methods=['POST', 'GET'])
def view_select_delivery(iin, num_order):
    # if 'result' not in session:
    #     redirect(url_for('view_index'))
    # log.info(f"DELIVERY STARTED. {session['iin']} ")
    status, result = get_status(num_order, iin)
    log.info(f"DELIVERY STARTED. iin: {iin}, num_order: {num_order}, status: {status}, result: {result} ")
    if status == 500:
        session['info'] = f"Техническая ошибка Сервиса! ИИН: {iin} Заказ №:{num_order}"
        return redirect(url_for('view_index'))
    if status == 0:
        session['info'] = f"Для ИИН: {iin} Заказ №:{num_order} отсутствует"
        return redirect(url_for('view_index'))
    session['result'] = result
    # log.info(f"------> DELIVERY SESSION RESULT: {session['result']}")
    return render_template("select_delivery.html", iin=session['iin'], url_my_khat=cfg.myKHAT_host)


@app.route('/', methods=['POST', 'GET'])
def view_index():
    if request.method == "POST":
        num_order = request.form['num_order']
        iin = request.form['iin']
        if num_order and iin:
            print(f'Получен запрос с номером заявки: {num_order}, iin: {iin}')
            session['iin'] = iin
            session['num_order'] = num_order
            return redirect(url_for('view_select_delivery', iin=iin, num_order=num_order))
        else:
            session['info'] = f'Не введен номер Заказа или ИИН'
    info = ''
    if 'info' in session:
        info = session['info']
        session.pop('info')
    if 'result' in session:
        session.pop('result')
    return render_template("index.html", info=info)

