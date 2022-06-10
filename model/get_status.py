from main_app import log
import app_config as cfg
import requests
import json


# {'data': {'requestId': '002226651471', 'resultCode': 'OK',
#           'serviceType': {'code': 'Z21-74', 'nameRu': 'Выдача справки о рождении', 'nameKz': 'Туылуы туралы анықтама беру'},
#           'organization': {'code': 'MJ-Z-A-S1', 'nameRu': 'Отдел № 2 Сарыаркинского района по обслуживанию населения филиала некоммерческого акционерного общества «Государственная корпорация «Правительство для граждан» по городу Нур-Султан', 'nameKz': '«Азаматтарға арналған үкімет» мемлекеттік корпорациясы» коммерциялық емес акционерлік қоғамының Нұр-Сұлтан қаласы бойынша филиалының Халыққа қызмет көрсету бойынша Сарыарқа аудандық № 2 бөлімі'},
#           'regionCode': None, 'street': None, 'house': None, 'flat': None, 'phone': None, 'addressDetail': None, 'firstName': None, 'lastName': None, 'middleName': None, 'iin': None},
#           'status': 'success', 'message': None}
def get_status_data(resp_json):
    result = {}
    try:
        data = resp_json['data']
        result['iin'] = data['iin']
        result['num_order'] = data['requestId']
        log.info(f"1. GET STATUS DATA. num_order: {result['num_order']}, iin: {result['iin']}, order: {result['num_order']}")
        serviceType = data['serviceType']
        if serviceType:
            result['serviceCode'] = serviceType['code']
            result['serviceNameRu'] = serviceType['nameRu']
            result['serviceNameKz'] = serviceType['nameKz']
        organization = data['organization']
        if organization:
            result['orgCode'] = organization['code']
            result['org_nameRu'] = organization['nameRu']
            result['org_nameKz'] = organization['nameKz']
        result['resultCode'] = data['resultCode']
        result['regionCode'] = data['regionCode']
        result['street'] = data['street']
        result['house'] = data['house']
        result['flat'] = data['flat']
        result['phone'] = data['phone']
        result['addressDetail'] = data['addressDetail']
        result['status'] = resp_json['status']
        result['message'] = resp_json['message']
        result['lastname'] = data['lastName']
        result['firstname'] = data['firstName']
        result['middlename'] = data['middleName']
    except Exception as e:
        log.error(f"ERROR. GET STATUS DATA: {result['num_order']} : {result['iin']}. Error: {e}")
    finally:
        return result


def get_status_order(resp_json):
    result = {}
    order = resp_json['order']
    ido = order['id']
    result['iin'] = order['iin']
    result['num_order'] = order['originalOrderNumber']
    log.info(f"1. GET STATUS ORDER. num_order: {result['num_order']}, iin: {result['iin']}, order: {order}")
    result['ext_num_order'] = order['externalOrderNumber']
    result['street'] = order['street']
    result['house'] = order['house']
    result['flat'] = order['flat']
    result['iscash'] = order['iscash']
    result['iscash'] = order['iscash']
    result['addressdetail'] = order['addressdetail']
    result['firstname'] = order['firstname']
    result['lastname'] = order['lastname']
    result['middlename'] = order['middlename']
    result['phone'] = order['contacts']
    result['regioncode'] = order['regioncode']
    result['statuscode'] = order['statuscode']
    result['statusdesc'] = order['statusdesc']
    result['courier'] = order['courier']
    result['orderStatusUpdates'] = order['orderStatusUpdates']
    result['payments'] = order['payments']
    if type(order["shepOrderData"]) is str:
        shepOrderData = json.loads(order['shepOrderData'])
    else:
        shepOrderData = order['shepOrderData']
    if shepOrderData:
        result['shepNumOrder'] = shepOrderData['requestId']
        result['shepResultCode'] = shepOrderData['resultCode']
        serviceType = shepOrderData['serviceType']
        if serviceType:
            result['serviceCode'] = serviceType['code']
            result['serviceNameRu'] = serviceType['nameRu']
            result['serviceNameKz'] = serviceType['nameKz']
        organization = shepOrderData['organization']
        if organization:
            result['orgCode'] = organization['code']
            result['org_nameRu'] = organization['nameRu']
            result['org_nameKz'] = organization['nameKz']
        result['regionCode'] = shepOrderData['regionCode']
        result['street'] = shepOrderData['street']
        result['house'] = shepOrderData['house']
        result['flat'] = shepOrderData['flat']
        result['shep_phone'] = shepOrderData['phone']
        result['addressDetail'] = shepOrderData['addressDetail']
        result['shep_firstName'] = shepOrderData['firstName']
        result['shep_lastName'] = shepOrderData['lastName']
        result['shep_middleName'] = shepOrderData['middleName']
        result['shep_iin'] = shepOrderData['iin']
    return result


def get_status(num_order, iin):
    url = f'http://{cfg.status_host}:{cfg.status_port}/ddocs/api/v1/find/{iin}/{num_order}'
    status = 0
    result = {}
    try:
        log.info(f"1. SERVICE REQUEST: num_order: '{num_order}', iin: {iin}, url: {url}")
        resp = requests.get(url)
        if resp.status_code != 200:
            status = resp.status_code
            return
        resp_json = resp.json()
        log.info(f"2. SERVICE REQUEST: num_order: '{num_order}', iin: {iin}, url: {resp_json}")
        if 'order' in resp_json:
            result = get_status_order(resp_json)
            status = 1
            if 'orderStatuses' in resp_json:
                result['order_Statuses'] = resp_json['orderStatuses']
        elif 'data' in resp_json:
            result = get_status_data(resp_json)
            if 'resultCode' in result and result['resultCode'] == 'OK':
                status = 1
        else:
            status = -1
        resp.close()
    except Exception as e:
        status = resp.status_code
        log.error(f"=====> ERROR REQUEST: {num_order} : {iin}. resp.status_code: {resp.status_code}, error: {e}")
    finally:
        log.info(f"GET STATUS. STATUS: {status}, RESULT: {result}")
        return status, result
