from delivery_parameter import using, app_name


if using == 'DEV_WIN_HOME':
    BASE = f'D:/Shamil/{app_name}'
elif using == 'DEV_WIN':
    BASE = f'C:/Shamil/{app_name}'
else:
    BASE = f'/home/cut_pdf/{app_name}'

if using[0:7] != 'DEV_WIN':
    host = 'notes1.gov4c.kz'
    os = 'unix'
    debug_level = 2
    FACE_CONTROL_ENABLE = True
    port = 5000
else:
    os = '!unix'
    debug_level = 4
    FACE_CONTROL_ENABLE = True
    host = 'localhost'
    port = 80

service_host = 'notes1.gov4c.kz'
service_port = 5001
LOG_FILE = f'{BASE}/pdd.log'
SPOOL = f'{BASE}/spool'
debug = True
trace_malloc = False

print(f"=====> CONFIG. using: {using}, BASE: {BASE}, app_name: {app_name}")

