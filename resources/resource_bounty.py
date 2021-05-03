#      Author: Birnadin Erick
#      Copyright © 2021. All rights are reserved by Birnadin Erick.
#      This script can be used without any written acknowledgement from author for personal or commercial purpose.
#

from datetime import datetime as d

from flask import abort
from flask_restful.reqparse import RequestParser
from flask_restful import Resource

from utility.helpers import create_id
from utility.mongo_api import mdb_api

bounties = mdb_api["BugBounty"]["Bounties"]

b_post_args = RequestParser()
b_get_args = RequestParser()
b_patch_args = RequestParser()
b_del_args = RequestParser()

b_post_args.add_argument("boname", type=str, help="BO_404_bn", required=True)
b_post_args.add_argument("bs", type=str, help="BO_404_bs")
b_post_args.add_argument("cid", type=int, help="BO_404_cid")
b_post_args.add_argument("dl", type=float, help="BO_404_dl")

b_get_args.add_argument("bo_id", type=int, help="BO_404_boid", required=True)

b_patch_args.add_argument("bo_id", type=int, help="BO_404_boid", required=True)
b_patch_args.add_argument("opts", type=str, help="BO_404_o", required=True)
b_patch_args.add_argument("params", type=str, help="BO_404_p", required=True)
b_patch_args.add_argument("poly", type=int, help="BO_404_poly", required=True)

b_del_args.add_argument("bo_id", type=int, help="BO_404_boid", required=True)


class ResourceBounty(Resource):
    @staticmethod
    def post():
        args = b_post_args.parse_args()
        bs = list()
        if args["bs"]:
            bs = [int(b) for b in args["bs"].split(",")]

        bounty = {
            '_id': create_id(args["boname"]),
            'boname': args["boname"],
            'bs': bs,
            'cstamp': d.now().timestamp()
        }
        if args["cid"]:
            bounty['cid'] = args["cid"]
        if args["dl"]:
            bounty['dl'] = args["dl"]

        try:
            b = bounties.insert_one(bounty)
        except Exception as e:
            abort(500, e.__str__())
        else:
            del args, bs, bounty
            return bounties.find_one({'_id': b.inserted_id}), 201

    @staticmethod
    def get():
        pass

    def patch(self):
        pass

    @staticmethod
    def delete():
        pass

    @staticmethod
    def update_per_opt(opt, arg, bo_id):
        pass
