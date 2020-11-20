from chatbot_api.ext.db import config
from flask_restful import Resource, reqparse


class Home(Resource):
    def get(self):
        return {'message': 'Server Start'}