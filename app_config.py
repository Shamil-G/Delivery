from delivery_parameter import using, app_name


if using == 'DEV_WIN_HOME':
    BASE = f'D:/Shamil/{app_name}'
elif using == 'DEV_WIN':
    BASE = f'C:/Shamil/{app_name}'
else:
    BASE = f'/home/delivery/{app_name}'

if using[0:7] != 'DEV_WIN':
    host = 'express.gov4c.kz'
    os = 'unix'
    debug_level = 2
    FACE_CONTROL_ENABLE = True
    port = 5050
else:
    os = '!unix'
    debug_level = 4
    FACE_CONTROL_ENABLE = True
    host = 'localhost'
    port = 80


status_host = 'express.gov4c.kz'
status_port = 80
LOG_FILE = f'{BASE}/delivery.log'
SPOOL = f'{BASE}/spool'
debug = True
trace_malloc = False
language = 'ru'
src_lang = 'file'
myKHAT_host = "http://express.gov4c.kz/mykhat"
YANDEX_host = 'https://express.insol.kz/svcapi/api/IntegrationMvc/CallbackV2'


print(f"=====> CONFIG. using: {using}, BASE: {BASE}, app_name: {app_name}")


