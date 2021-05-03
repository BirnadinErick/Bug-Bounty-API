#      Author: Birnadin Erick
#      Copyright © 2021. All rights are reserved by Birnadin Erick.
#      This script can be used without any written acknowledgement from author for personal or commercial purpose.
#
from flask import Flask
from flask_restful import Api

from resource_bounty import ResourceBounty
from resource_clan import ResourceClan
from resources.resource_bug import ResourceBug
from resources.resource_hunter import ResourceHunter

app = Flask(__name__)  # app init
api = Api(app)  # api init


api.add_resource(ResourceBug, '/bug')
api.add_resource(ResourceHunter, '/hunter')
api.add_resource(ResourceClan, '/clan')
api.add_resource(ResourceBounty, '/bounty')

if __name__ == '__main__':
    app.run()
