from datetime import datetime as dt
from time import sleep

from flask import abort
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from pymongo.errors import DocumentTooLarge, DuplicateKeyError, NetworkTimeout, OperationFailure, CollectionInvalid, \
    ConnectionFailure

from utility.helpers import create_id
from utility.mongo_api import mdb_api, reconnect

bugs = mdb_api['BugBounty']['Bugs']

bug_post_args = RequestParser()
bug_get_args = RequestParser()
bug_patch_args = RequestParser()
bug_del_args = RequestParser()

# TODO: add new error codes to the notebook
bug_post_args.add_argument("name", type=str, help="B_404_name", required=True)
bug_post_args.add_argument("author", type=int, help="B_404_auth", required=True)
bug_post_args.add_argument("bounty_id", type=int, help="B_404_bounty", required=True)
bug_post_args.add_argument("desc", type=str, help="B_404_auth")

bug_get_args.add_argument("bug_id", type=int, help="B_404_bid",
                          required=True)

bug_patch_args.add_argument("bug_id", type=int, help="B_404_bid", required=True)
bug_patch_args.add_argument("opt", type=int, help="B_404_opt", required=True)
bug_patch_args.add_argument("param", type=str, help="B_404_p", required=True)
bug_patch_args.add_argument("poly", type=int, help="B_404_m", required=True)
bug_patch_args.add_argument("opts", type=str)

bug_del_args.add_argument("bug_id", type=int, help="B_404_b-d", required=True)


class ResourceBug(Resource):
    @staticmethod
    def post():
        """
        TODO: validate author and bouty_id 
        """
        args = bug_post_args.parse_args()
        times = 0
        bug = {
            "_id": create_id(args["name"]),
            "name": args["name"],
            "status": 1,
            "author": args["author"],
            "c_date": dt.now().ctime(),
            "b_id": args["bounty_id"],
            "desc": args["desc"],
            "assignees": []
        }

        while True:
            try:
                b = bugs.insert_one(bug)
            except DocumentTooLarge:
                if times:
                    abort(413, "Sorry, document too larg to produce")
                else:
                    del (bug["desc"])
                    times += 1
                    continue
            except DuplicateKeyError:
                bug["_id"] = create_id(args["name"])
                continue
            except NetworkTimeout:
                if times:
                    times += 1
                    sleep(500)
                    continue
                else:
                    abort(503, "Sorry, something went wrong")
            except OperationFailure as e:
                abort(503, e.__str__())
            except CollectionInvalid:
                abort(503, "Sorry, something went wrong")
            except ConnectionFailure:
                if times:
                    reconnect()
                    continue
                else:
                    abort(503, "Sorry, something went wrong")
            else:
                bug['_id'] = b.inserted_id
                return bug, 201
            finally:
                del b

    @staticmethod
    def get():
        args = bug_get_args.parse_args()
        times = 0
        while True:
            try:
                bug = bugs.find_one({'_id': {'$eq': args["bug_id"]}})
            except NetworkTimeout:
                if times:
                    times += 1
                    sleep(500)
                    continue
                else:
                    abort(503, "Sorry, something went wrong")
            except OperationFailure as e:
                abort(503, e.__str__())
            except CollectionInvalid:
                abort(503, "Sorry, something went wrong")
            except ConnectionFailure:
                if times:
                    reconnect()
                    continue
                else:
                    abort(503, "Sorry, something went wrong")

            else:
                if bug:
                    return bug, 200
                else:
                    abort(404, "Bug you tried to obtain for, is not found. May be deleted?")

            finally:
                del bug

    @staticmethod
    def patch():
        """
        patchable attr.s:
            ~ stat       --> 0
            ~ assignee/s --> 1
            ~ desc       --> 2
            ~ bounty_id  --> 3
        """
        args = bug_patch_args.parse_args()

        if not args["poly"]:
            update_per_opt(opt=args["opt"], param=args["param"], bug_id=args["bug_id"])
        else:
            if args["opts"]:
                opts = [int(o) for o in args["opts"].split("|")]
                params = args["param"].split("|")
                for opt in opts:
                    update_per_opt(opt=opt, param=params[opts.index(opt)], bug_id=args["bug_id"])
            else:
                abort(403, "Opts param should be specified if Poly is true")

        bug = bugs.find_one({'_id': args["bug_id"]})
        return bug, 200

    @staticmethod
    def delete():
        args = bug_del_args.parse_args()
        times = 0
        while True:
            try:
                bugs.delete_one({'_id': {'$eq': args["bug_id"]}})
            except NetworkTimeout:
                if times:
                    times += 1
                    sleep(500)
                    continue
                else:
                    abort(503, "Sorry, something went wrong")
            except OperationFailure as e:
                abort(503, e.__str__())
            except CollectionInvalid:
                abort(503, "Sorry, something went wrong")
            except ConnectionFailure:
                if times:
                    reconnect()
                    continue
                else:
                    abort(503, "Sorry, something went wrong")

            else:
                del times
                return {'deleted_id': args["bug_id"], "status": "succeded"}, 200

        del args


# noinspection PyUnboundLocalVariable,PyUnusedLocal
def update_per_opt(opt, param, bug_id):
    if opt == 0:
        stat = int(param)
        if (stat < 0) or (stat > 1):
            abort(403, "Please make sure the status value pointing is correct!")
        else:
            try:
                bugs.update_one(
                    {'_id': {'$eq': bug_id}},
                    {'$set': {'status': stat}}
                )
            except Exception as e:
                abort(500, e.__str__())
            else:
                del stat

    elif opt == 1:
        a_list = list()
        if "," in param:
            a_list = [int(a) for a in param.split(",")]
        else:
            if len(param) > 1:
                a_list.append(int(param))
            else:
                a_list = []
        # noinspection PyUnboundLocalVariable
        if len(a_list):
            try:
                bugs.update_one(
                    {'_id': {'$eq': bug_id}},
                    {'$set': {'assignees': a_list}}
                )
            except Exception as e:
                abort(500, e.__str__())
            else:
                del a_list

    elif opt == 2:
        try:
            bugs.update_one(
                {'_id': {'$eq': bug_id}},
                {'$set': {'desc': param}}
            )
        except Exception as e:
            abort(500, e.__str__())

    elif opt == 3:
        b_id = int(param)
        try:
            bugs.update_one(
                {'_id': {'$eq': bug_id}},
                {'$set': {'b_id': b_id}}
            )
        except Exception as e:
            abort(500, e.__str__())
        else:
            del b_id
    else:
        abort(403, "Please make sure the opt you opted is available")


if __name__ == '__main__':
    from utility.exceptions import UseAsModule

    raise UseAsModule
