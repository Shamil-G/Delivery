from main_app import log
import app_config as cfg
import requests
import json


def get_status(num_order, iin):
    url = f'http://{cfg.status_host}:{cfg.status_port}/ddocs/api/v1/find/{iin}/{num_order}'
    status = 0
    resp_json = ''
    result = {}
    try:
        log.info(f"SERVICE REQUEST: num_order: '{num_order}', iin: {iin}, url: {url}")
        resp = requests.get(url)
        resp_json = resp.json()
        log.info(f"2. SERVICE REQUEST: num_order: '{num_order}', iin: {iin}, url: {resp_json}")
        if 'orderStatuses' in resp_json:
            result['order_Statuses'] = resp_json['orderStatuses']
        if 'order' in resp_json:
            order = resp_json['order']
            ido = order['id']
            result['iin'] = order['iin']
            result['num_order'] = order['originalOrderNumber']
            # log.info(f"3. SERVICE REQUEST: num_order: '{num_order}', iin: {iin}, order: {order}")
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
            result['contacts'] = order['contacts']
            result['regioncode'] = order['regioncode']
            result['statuscode'] = order['statuscode']
            result['statusdesc'] = order['statusdesc']
            result['courier'] = order['courier']
            result['orderStatusUpdates'] = order['orderStatusUpdates']
            result['payments'] = order['payments']
            print(f'------>>> Type order: {type(order["shepOrderData"])}')
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
            status = 1
        log.info(f"SERVICE RESPONSE. Resp: {resp_json}")
        resp.close()
    except Exception as e:
        log.error(f"=====> ERROR REQUEST: {num_order} : {iin}. error: {e}")
    finally:
        return status, result
