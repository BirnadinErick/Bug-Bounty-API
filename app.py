from flask import Flask
from flask_restful import Api

from resources.resource_bug import ResourceBug

app = Flask(__name__)  # app init
api = Api(app)  # api init


api.add_resource(ResourceBug, '/bug')

if __name__ == '__main__':
    app.run()
