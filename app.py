from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DebugServer
from CustomJSONEncoder import CustomJSONEncoder


app = Flask(__name__)
app.config.from_object(DebugServer)

db = SQLAlchemy(app)
app.secret_key = 'blahblahblah'
app.json_encoder = CustomJSONEncoder







