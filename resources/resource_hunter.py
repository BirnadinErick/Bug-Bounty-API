#      Author: Birnadin Erick
#      Copyright © 2021. All rights are reserved by Birnadin Erick.
#      This script can be used without any written acknowledgement from author for personal or commercial purpose.
#
from datetime import datetime

from flask import abort
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from utility.helpers import hash_passwd, create_id, verify_passwd
from utility.mongo_api import mdb_api

hunters = mdb_api["BugBounty"]["Hunters"]

hunter_post_args = RequestParser()
hunter_get_args = RequestParser()
hunter_patch_args = RequestParser()
hunter_del_args = RequestParser()

hunter_post_args.add_argument("hname", type=str, help="H_404_hn", required=True)
hunter_post_args.add_argument("ptxt", type=str, help="H_404_ptxt", required=True)
hunter_post_args.add_argument("fname", type=str, help="H_404_fn", required=True)
hunter_post_args.add_argument("lname", type=str)

hunter_get_args.add_argument("h_id", type=int, help="U_404_hid", required=True)

hunter_patch_args.add_argument("h_id", type=int, help="H_404_hid", required=True)
hunter_patch_args.add_argument("poly", type=int, help="H_404_poly", required=True)
hunter_patch_args.add_argument("opts", type=str, help="H_404_opt", required=True)
hunter_patch_args.add_argument("params", type=str, help="H_404_p", required=True)

hunter_del_args.add_argument("h_id", type=int, help="H_404_hid", required=True)
hunter_del_args.add_argument("ptxt", type=str, help="H_404_ptxt", required=True)


class ResourceHunter(Resource):
    @staticmethod
    def post():
        args = hunter_post_args.parse_args()
        h = hunters.find_one({'hname': {'$eq': args["hname"]}})

        try:
            if h.inserted_id:
                abort(409, "H_409_hn_taken")
        except AttributeError:
            pass

        hunter = {
            '_id': create_id(args["hname"]),
            'hname': args["hname"],
            'fname': args["fname"],
            'phash': hash_passwd(args["ptxt"]),
            'ctime': datetime.now().ctime(),
            'c_ids': [],
            'bo_ids': []
        }

        if args["lname"]:
            hunter["lname"] = args["lname"]

        try:
            hunters.insert_one(hunter)
        except Exception as e:
            abort(501, e.__str__())
        else:
            del hunter['phash']
            return hunter, 201

    @staticmethod
    def get():
        # TODO: authenticate the req b4 processing via utility uri
        args = hunter_get_args.parse_args()
        try:
            hunter = hunters.find_one({'_id': {'$eq': args["h_id"]}})
            if hunter is not None:
                del hunter["phash"]
            else:
                abort(404, "Hunter you askes for may have been deleted?!")
        except Exception as e:
            abort(500, e.__str__())
        else:
            del args
            return hunter, 200

    def patch(self):
        """
        TODO: authenticate the req b4 processing via utility uri
        patchable attrs:-
            ~ b_ids --> 0
            ~ c_ids --> 1
            ~ lname --> 2
            ~ fname --> 3
            ~ ptxt  --> 4
        """
        args = hunter_patch_args.parse_args()

        if not args["poly"]:
            self.update_per_opt(
                opt=int(args["opts"]),
                arg=args["params"],
                h_id=args["h_id"]
            )
        else:
            os = [int(o) for o in args["opts"].split("|")]
            ps = args["params"].split("|")
            for o in os:
                self.update_per_opt(
                    opt=o,
                    arg=ps[os.index(o)],
                    h_id=args["h_id"]
                )

        h = hunters.find_one({'_id': args["h_id"]})
        del h["phash"]
        return h, 200

    @staticmethod
    def delete():
        args = hunter_del_args.parse_args()
        h = hunters.find_one({'_id': args["h_id"]})
        if verify_passwd(args["ptxt"], h['phash']):
            try:
                hunters.delete_one({'_id': {'$eq': args["h_id"]}})
            except Exception as e:
                abort(500, e.__str__())
            else:
                return "deletion success", 200
        abort(403, "U_403_xpass")

    @staticmethod
    def update_per_opt(opt, arg, h_id):
        if opt == 0:
            try:
                if "," in arg:
                    b_ids = [int(b) for b in arg.split(",")]
                else:
                    b_ids = [int(arg)]

                hunters.update_one(
                    {'_id': {'$eq': h_id}},
                    {'$set': {'b_ids': b_ids}}
                )
            except AttributeError or TypeError:
                abort(403, "U_403_p")
            except Exception as e:
                abort(500, e.__str__())

        elif opt == 1:
            try:
                if "," in arg:
                    c_ids = [int(b) for b in arg.split(",")]
                else:
                    c_ids = [int(arg)]

                hunters.update_one(
                    {'_id': {'$eq': h_id}},
                    {'$set': {'c_ids': c_ids}}
                )
            except AttributeError or TypeError:
                abort(403, "U_403_p")
            except Exception as e:
                abort(500, e.__str__())

        elif opt == 2:
            try:
                hunters.update_one(
                    {'_id': {'$eq': h_id}},
                    {'$set': {'lname': arg}}
                )
            except Exception as e:
                abort(500, e.__str__())

        elif opt == 3:
            try:
                hunters.update_one(
                    {'_id': {'$eq': h_id}},
                    {'$set': {'fname': arg}}
                )
            except Exception as e:
                abort(500, e.__str__())

        elif opt == 4:
            try:
                if "," in arg:
                    ins = arg.split(",")
                    if len(ins) < 2:
                        abort(403, "U_403_p")

                    h = hunters.find_one({'_id': {'$eq': h_id}})

                    if verify_passwd(ins[0], h['phash']):
                        hunters.update_one(
                            {'_id': {'$eq': h_id}},
                            {'$set': {'phash': hash_passwd(ins[1])}}
                        )
                        del h, ins
                    else:
                        del h, ins
                        abort(403, "Wrong Current Password")
                else:
                    abort(403, "U_403_p")
            except Exception as e:
                abort(500, e.__str__())

        else:
            abort(403, "U_403_p")
