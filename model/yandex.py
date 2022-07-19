from main_app import log
import app_config as cfg
from flask import session
import requests
# import json


def request_yandex():
    url = cfg.YANDEX_host
    result = session['result']

    req_s = {'iin': session['iin'],
             'requestId': session['num_order'],
             'firstname': result['firstname'],
             'lastname': result['lastname'],
             'middlename': result['middlename'],
             'phone': result['phone'],
             'organization': {
                 'code': result['orgCode'],
                 'nameRu': result['org_nameRu'],
                 'nameKz': result['org_nameKz']
             },
             'serviceType': {
                 'code': result['serviceCode'],
                 'nameRu': result['serviceNameRu'],
                 'nameKz': result['serviceNameKz']
             }
             }

    log.info(f"---> REQ_S: {req_s}")

    resp = requests.post(url, json=req_s)
    if resp.status_code == 200:
        resp_json = resp.json()
        if 'callbackUrl' in resp_json:
            new_url = resp_json['callbackUrl']
            return new_url
    log.error(f"===> ERROR YANDEX. resp: {resp.status_code}")
    return ''
