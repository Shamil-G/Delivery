from delivery_parameter import using
from flask import Flask
from util.logger import log


app = Flask(__name__)
app.secret_key = 'Delivery secret key:askjv;asdkvp512-vhasd'

log.info("__INIT MAIN APP__ started")
print("__INIT MAIN APP__ started")

