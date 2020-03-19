# from models import QuizSession, Card
from flask import json


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if o.__class__.__name__ == 'QuizSession':
            return o.to_json()
        if o.__class__.__name__ == 'Card':
            return o.to_json()
        return json.JSONEncoder.default(self, o)
