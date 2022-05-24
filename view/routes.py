from flask import render_template, make_response, request
from util.utils import *
from main_app import app, log
import app_config as cfg
import datetime
import requests
import json

def save_doc_to_file(url, text):
    if os.path.exists(url):
        os.remove(url)
    with open(url, "wb") as file:
        file.write(text)
    log.info(f"------>SAVED PDF TO FILE: {url}")


def get_pdf(appId, lang):
    url = f'http://{cfg.service_host}:{cfg.service_port}/ipsc/receipt.sv?lang={lang}&appId={appId}'
    success = 0
    try:
        resp = requests.get(url)
        resp_text = resp.content
        resp.close()
        save_doc_to_file(f'{cfg.SPOOL}/{appId}.pdf', resp_text)
        del resp_text
        success = 1
        # log.info(f'-----> GET PDF. appId: {appId}, lang: {lang}, url: {url}')
    except requests.exceptions.Timeout as errT:
        log.error(f'ERROR TIMEOUT. SEND RESULT TO ARM GO. num_order: {appId} : {errT}')
    except requests.exceptions.TooManyRedirects as errM:
        log.error(f'ERROR MANY REDIRECT. SEND RESULT TO ARM GO. num_order: {appId} : {errM}')
    except requests.exceptions.ConnectionError as errC:
        log.error(f'ERROR Connection. SEND RESULT TO ARM GO. num_order: {appId} : {errC}')
    except requests.exceptions.RequestException as errE:
        log.error(f'ERROR Exception. SEND RESULT TO ARM GO. num_order: {appId} : {errE}')
    except Exception as ex:
        log.error(f'ERROR Exception. SEND RESULT TO ARM GO. num_order: {appId} : {ex}')
    finally:
        return success


#

def get_status(num_order, iin):
    url = f'http://{cfg.status_host}:{cfg.status_port}/ddocs/api/v1/find/{iin}/{num_order}'
    status = 0
    try:
        log.info(f"SERVICE REQUEST: num_order: '{num_order}', iin: {iin}, url: {url}")
        resp = requests.get(url)
        resp_json = resp.json()
        order_Statuses = ''
        order = ''
        if 'orderStatuses' in resp_json:
            order_Statuses = resp_json['orderStatuses']
        if 'order' in resp_json:
            order = resp_json['order']
            ido = order['id']
            origOrderNum = order['originalOrderNumber']
            extOrderNum = order['externalOrderNumber']
            street = order['street']
            house = order['house']
            flat = order['flat']
            iscash = order['iscash']
            addressdetail = order['addressdetail']
            firstname = order['firstname']
            lastname = order['lastname']
            middlename = order['middlename']
            contacts = order['contacts']
            regioncode = order['regioncode']
            statuscode = order['statuscode']
            statusdesc = order['statusdesc']
            courier = order['courier']
            orderStatusUpdates = order['orderStatusUpdates']
            payments = order['payments']
            print(f'------>>> Type order: {type(order["shepOrderData"])}')
            if type(order["shepOrderData"]) is str:
                shepOrderData = json.loads(order['shepOrderData'])
            else:
                shepOrderData = order['shepOrderData']
            if shepOrderData:
                requestId = shepOrderData['requestId']
                resultCode = shepOrderData['resultCode']
                serviceType = shepOrderData['serviceType']
                if serviceType:
                    code = serviceType['code']
                    nameRu = serviceType['nameRu']
                    nameKz = serviceType['nameKz']
                organization = shepOrderData['organization']
                if organization:
                    org_code = organization['code']
                    org_nameRu = organization['nameRu']
                    org_nameKz = organization['nameKz']
                regionCode = shepOrderData['regionCode']
                shep_street = shepOrderData['street']
                shep_house = shepOrderData['house']
                shep_flat = shepOrderData['flat']
                shep_phone = shepOrderData['phone']
                shep_addressDetail = shepOrderData['addressDetail']
                shep_firstName = shepOrderData['firstName']
                shep_lastName = shepOrderData['lastName']
                shep_middleName = shepOrderData['middleName']
                shep_iin = shepOrderData['iin']
        log.info(f"SERVICE RESPONSE. Resp: {resp_json}")
        # print(f'-----> resp: {resp_text}')
        resp.close()
        status = 1
    except Exception as e:
        log.error(f"=====> ERROR REQUEST: {num_order} : {iin}. error: {e}")
    finally:
        return status


# https://notes.gov4c.kz/ipsc/receipt.sv?lang=ru&appId=002224748721
@app.route('/', methods=['POST', 'GET'])
def view_index():
    if request.method == "POST":
        num_order = request.form['num_order']
        iin = request.form['iin']
        print(f'Получен запрос с номером заявки: {num_order}, iin: {iin}')
        if num_order and iin:
            get_status(num_order, iin)
    return render_template("index.html")

