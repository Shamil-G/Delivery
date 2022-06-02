import requests


def request_soap():
    # SOAP request URL
    url = "https://www.nitec.kz/index.php/post/integrirovannaya-informatsionnaya-sistema-dlyatsentrov-obslujivaniya - naseleniya - tson"
    # structured XML
    payload = """<?xml version="1.0" encoding="UTF-8"?>
            <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
                <SOAP-ENV:Header xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"/>
                <S:Body>
                    <ns2:SendMessage xmlns:ns2="http://bip.bee.kz/SyncChannel/v10/Types">
                        <request>
                            <requestInfo>
                                <messageId>123456789</messageId>
                                <serviceId>SR05CONSynchService</serviceId>
                                <messageDate>2019-12-31T18:18:49.864+06:00</messageDate>
                                <sender>
                                    <senderId>test</senderId>
                                    <password>test</password>
                                </sender>
                            </requestInfo>
                            <requestData>
                                <data>
                                    <checkApplicationIINRequest:checkApplicationIINRequest xmlns:checkApplicationIINRequest="http://schemas.letograf.kz/iiscon/bus/v1" xmlns="http://schemas.letograf.kz/iiscon/bus/v1">
                                        <requestId>123456789</requestId>
                                        <requestIIN>777777777777</requestIIN>
                                    </checkApplicationIINRequest:checkApplicationIINRequest>
                                </data>
                            </requestData>
                        </request>
                    </ns2:SendMessage>
                </S:Body>
            </S:Envelope>"""
    # headers
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }
    # POST request
    response = requests.request("POST", url, headers=headers, data=payload)

    # prints the response
    print(response.text)
    print(response)


if __name__ == "__main__":
    request_soap()
    # log.info(f"===> Main Delivery started on {cfg.host}:{cfg.port}, work_dir: {cfg.BASE}")
