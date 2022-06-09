from main_app import log
import app_config as cfg
from flask import redirect, url_for, session
import requests
import json


def request_yandex():
    url = cfg.YANDEX_host
    result = session['result']
    iin = session['iin']
    num_order = session['num_order']
    # print(f"---> iin: {iin}, order: {num_order}")
    # print(f"1. REQUEST_YANDEX: {iin} : {num_order}, {result['firstname']} : {result['lastname']}, {result['contacts']}")
    # print(f"2. REQUEST_YANDEX: {result['statusdesc']}, {result['flat']}, {result['addressdetail']}")
    # print(f"3. REQUEST_YANDEX: {result['serviceCode']}, {result['serviceNameRu']}, {result['serviceNameKz']}")
    # print(f"4. REQUEST_YANDEX: {result['orgCode']}, {result['org_nameRu']}, {result['org_nameKz']}")

    # '"statusdesc": "' + result['statusdesc'] + '", "flat": "' + result['flat'] + '", "addressdetail": "' + \
    # result['addressdetail'] + '", '
    # add_s =
    # req_s = '{'
    # req_s = '{"iin": "' + iin + '", "requestId": "' + num_order + '", ' \
    #         '"firstname": "'+result['firstname']+'", "lastname": "'+result['lastname']+'", ' \
    #         '"contacts": "'+result['contacts']+'", ' \
    #         '"serviceType": {"code": "'+result['serviceCode']+'", "nameRu": "'+result['serviceNameRu']+'", ' \
    #         '"nameKz": "'+result['serviceNameKz']+'"}, ' \
    #         '"organization": {"code": "'+result['orgCode']+'", "nameRu": "'+result['org_nameRu']+'", ' \
    #         '"nameKz": "'+result['org_nameKz']+'" ' \
    #         '}}'
    fio_s = ''
    if 'firstname' in result and result['firstname'] is not None:
        fio_s = '"firstname": "'+result['firstname']+'", '
    if 'lastname' in result and result['lastname'] is not None:
        fio_s = fio_s + '"lastname": "'+result['lastname']+'", '
    if 'middlename' in result and result['middlename'] is not None:
        fio_s = fio_s + '"middlename": "'+result['middlename']+'", '
    if 'phone' in result and result['phone'] is not None:
        fio_s = fio_s + '"phone": "'+result['phone']+'", '

    req_s = '{"iin": "' + iin + '", "requestId": "' + num_order + '", ' + fio_s + \
            '"serviceType": {"code": "'+result['serviceCode']+'", "nameRu": "'+result['serviceNameRu'] + \
            '", "nameKz": "'+result['serviceNameKz'] + \
            '"}, "organization": {"code": "'+result['orgCode']+'", "nameRu": "'+result['org_nameRu'] + \
            '", "nameKz": "'+result['org_nameKz'] + \
            '"}}'

    # print(f"---------> Yandex req_json2: {req_s}")
    req_json2 = json.loads(req_s)
    # print(f"---------> Yandex req_json2: {req_json2}")
    resp = requests.post(url, json=req_json2)
    if resp.status_code == 200:
        resp_json = resp.json()
        if 'callbackUrl' in resp_json:
            new_url = resp_json['callbackUrl']
            # log.info(f"YANDEX. CALLBACK URL: {new_url}")
            return new_url
    log.error(f"ERROR YANDEX. resp: {resp.status_code}")
    return ''
