from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

from my_coin.routes import *
from my_coin.error_handler import register_error_handlers
register_error_handlers(app)