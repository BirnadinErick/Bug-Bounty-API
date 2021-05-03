#      Author: Birnadin Erick
#      Copyright © 2021. All rights are reserved by Birnadin Erick.
#      This script can be used without any written acknowledgement from author for personal or commercial purpose.

from datetime import datetime

from flask import abort
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from utility.helpers import create_id
from utility.mongo_api import mdb_api

clans = mdb_api["BugBounty"]["Clans"]

clan_post_args = RequestParser()
clan_get_args = RequestParser()
clan_patch_args = RequestParser()
clan_del_args = RequestParser()

clan_post_args.add_argument("cname", type=str, help="C_404_cn", required=True)
clan_post_args.add_argument("ls", type=str, help="C_404_l")
clan_post_args.add_argument("hs", type=str, help="C_404_h")

clan_get_args.add_argument("c_id", type=int, help="C_404_cid", required=True)

clan_patch_args.add_argument("c_id", type=int, help="C_404_cid", required=True)
clan_patch_args.add_argument("opts", type=str, help="C_404_o", required=True)
clan_patch_args.add_argument("poly", type=int, help="C_404_po", required=True)
clan_patch_args.add_argument("params", type=str, help="C_404_p", required=True)

clan_del_args.add_argument("c_id", type=int, help="C_404_cid", required=True)


class ResourceClan(Resource):
    # noinspection PyUnusedLocal
    @staticmethod
    def post():
        # TODO: add privileges to different leaders(ls) using OOP
        args = clan_post_args.parse_args()
        ls = list()
        hs = list()
        if args["ls"]:
            ls = [int(l) for l in args["ls"].split(",")]
        if args["hs"]:
            hs = [int(h) for h in args["hs"].split(",")]

        clan = {
            '_id': create_id(args["cname"]),
            'cname': args["cname"],
            'ctime': datetime.now().ctime(),
            'bs': []
        }
        if len(ls):
            clan['ls'] = ls
        if len(hs):
            clan['hs'] = hs

        try:
            clans.insert_one(clan)
        except Exception as e:
            abort(500, e.__str__())
        else:
            c = clans.find_one({'_id': {'$eq': clan['_id']}})
            del clan
            return c, 201

    @staticmethod
    def get():
        args = clan_get_args.parse_args()
        try:
            c = clans.find_one({'_id': {'$eq': args["c_id"]}})
        except Exception as e:
            abort(500, e.__str__())
        else:
            if c is None:
                abort(404, "C_404_xcid")
            else:
                return c, 200

    def patch(self):
        """
        pathcable attr.s:
            ~ cname --> 0
            ~ ls    --> 1
            ~ hs    --> 2
            ~ bs    --> 3
        """
        args = clan_patch_args.parse_args()
        if args["poly"]:
            os = [int(o) for o in args["opts"].split("|")]
            ps = [p for p in args["params"].split("|")]

            for o in os:
                self.update_per_opt(
                    opt=o,
                    arg=ps[os.index(o)],
                    c_id=args["c_id"]
                )
        else:
            self.update_per_opt(
                opt=int(args["opts"]),
                arg=args["params"],
                c_id=args["c_id"]
            )

        return clans.find_one({'_id': args["c_id"]}), 200

    @staticmethod
    def delete():
        args = clan_del_args.parse_args()
        try:
            clans.delete_one({'_id': args["c_id"]})
        except Exception as e:
            abort(500, e.__str__())
        else:
            return "deletion succeeded or clan not found", 200

    # noinspection DuplicatedCode
    @staticmethod
    def update_per_opt(opt, arg, c_id):
        if type(opt) != int:
            abort(403, "C_403_xp")

        if opt == 0:
            try:
                clans.update_one(
                    {'_id': {'$eq': c_id}},
                    {'$set': {'cname': arg}}
                )
            except Exception as e:
                abort(500, e.__str__())
            finally:
                del opt, arg, c_id

        elif opt == 1:
            ls = [int(l) for l in arg.split(",")]
            try:
                clans.update_one(
                    {'_id': {'$eq': c_id}},
                    {'$set': {'ls': ls}}
                )
            except Exception as e:
                abort(500, e.__str__())
            finally:
                del opt, arg, c_id

        elif opt == 2:
            hs = [int(h) for h in arg.split(",")]
            try:
                clans.update_one(
                    {'_id': {'$eq': c_id}},
                    {'$set': {'hs': hs}}
                )
            except Exception as e:
                abort(500, e.__str__())
            finally:
                del opt, arg, c_id

        elif opt == 3:
            bs = [int(b) for b in arg.split(",")]
            try:
                clans.update_one(
                    {'_id': {'$eq': c_id}},
                    {'$set': {'bs': bs}}
                )
            except Exception as e:
                abort(500, e.__str__())
            finally:
                del opt, arg, c_id

        else:
            abort(403, "C_403_xp")
