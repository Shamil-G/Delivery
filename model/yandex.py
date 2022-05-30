from main_app import log
import app_config as cfg
from flask import redirect, url_for, session
import requests
import json


def request_yandex():
    url = cfg.YANDEX_host
    iin = session['iin']
    num_order = session['num_order']
    # iin = "630901400075"
    # num_order = "002222946220"
    req_s = '{"iin": "' + iin + '", "requestId": "' + num_order + '", ' \
          '"serviceType": {"code": "Z21-74", "nameRu": "Выдача справки о рождении", ' \
          '"nameKz": "Туылуы туралы анықтама беру"}, ' \
          '"organization": {"code": "MJ-Z-A-A3", "nameRu": "Отдел № 1 Есильского района по обслуживанию населения ' \
          'филиала некоммерческого акционерного общества «Государственная корпорация «Правительство для граждан»", ' \
          '"nameKz": "«Азаматтарға арналған үкімет» мемлекеттік корпорациясы» коммерциялық емес акционерлік ' \
          'қоғамының Нұр-Сұлтан қаласы бойынша филиалының Халыққа қызмет көрсету\u00A0бойынша ' \
          'Есіл аудандық № 1 бөлімі" ' \
          '}}'
    req_json2 = json.loads(req_s)
    print(f"---------> Yandex req_json2: {req_json2}")
    resp = requests.post(url, json=req_json2)
    print(f"---------> Yandex resp: {resp}")
    resp_json = resp.json()
    if 'callbackUrl' in resp_json:
        new_url = resp_json['callbackUrl']
        print(f"---------> Yandex new_url: {new_url}")
        return new_url
