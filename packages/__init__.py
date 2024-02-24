from flask import Flask
from flask_cors import CORS

app = Flask(__name__, template_folder='../templates', static_folder='../static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from packages import backend