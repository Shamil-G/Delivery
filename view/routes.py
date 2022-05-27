from flask import render_template, session, redirect, url_for, make_response, request
from util.utils import *
from main_app import app, log
import app_config as cfg
from model.get_status import get_status
import requests
import json
from model.yandex import *


@app.route('/status_mykhat', methods=['POST', 'GET'])
def view_status_mykhat():
    if 'result' in session:
        result = session['result']
    else:
        return redirect(url_for('view_index'))
    print(f'STATUS_ORDER. {result} ')
    if request.method == "POST":
        print(f'Получена команда VIEW_ORDER')
        return redirect(url_for('view_index'))
    return render_template("status_mykhat.html", num_order=result['num_order'], iin=result['iin'],
                           courier=result['courier'], firstname=result['firstname'], lastname=result['lastname'],
                           phone=result['contacts'], shep_phone=result['shep_phone'],
                           org_nameRu=result['org_nameRu'],
                           serviceNameRu=result['serviceNameRu'],
                           addressDetail=result['addressDetail'], house=result['house'], flat=result['flat'],
                           status=result['statuscode'])


@app.route('/status_yandex', methods=['POST', 'GET'])
def view_status_yandex():
    if 'result' in session:
        result = session['result']
    else:
        return redirect(url_for('view_index'))
    new_url = request_yandex()
    print(f'redirect to: {new_url} ')
    return redirect(new_url)


@app.route('/new_order', methods=['POST', 'GET'])
def view_new_order():
    if 'result' in session:
        result = session['result']
    else:
        return redirect(url_for('view_index'))
    print(f'STATUS_ORDER. {result} ')
    if request.method == "POST":
        print(f'Получена команда VIEW_ORDER')
        return redirect(url_for('view_index'))
    return render_template("new_order.html", num_order=result['num_order'], iin=result['iin'],
                           firstname=result['firstname'], lastname=result['lastname'],
                           phone=result['contacts'],
                           org_nameRu=result['org_nameRu'],
                           serviceNameRu=result['serviceNameRu'])


@app.route('/delivery', methods=['POST', 'GET'])
def view_select_delivery():
    if 'result' not in session:
        redirect(url_for('view_index'))
    log.info(f"DELIVERY STARTED. {session['iin']} ")
    return render_template("select_delivery.html", iin=session['iin'])


# https://notes.gov4c.kz/ipsc/receipt.sv?lang=ru&appId=002224748721
@app.route('/', methods=['POST', 'GET'])
def view_index():
    if request.method == "POST":
        num_order = request.form['num_order']
        iin = request.form['iin']
        print(f'Получен запрос с номером заявки: {num_order}, iin: {iin}')
        if num_order and iin:
            status, result = get_status(num_order, iin)
            if status == 1:
                session['result'] = result
                # return redirect(url_for('view_select_delivery'))
                # return redirect(url_for('view_status_yandex'))
            else:
                return redirect(url_for('view_select_delivery'))
                # del result
    return render_template("index.html")

