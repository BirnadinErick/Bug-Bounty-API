def create_id(name):
    import datetime
    from math import ceil, floor
    now = ceil(datetime.datetime.now().timestamp())
    first_letter_int = ord(name[0])
    last_letter_int = ord(name[-1])
    _id_not_floor = now + (first_letter_int + last_letter_int) / len(name)
    return floor(_id_not_floor)


def hash_passwd(pwd):
    """
    utility func to hash a given passwd str for first time
    :param pwd:
    :return: bString
    """
    from os import urandom as salter
    from hashlib import pbkdf2_hmac as hasher

    salt = salter(64)
    key = hasher(
        'sha256',
        pwd.encode('utf-8'),
        salt,
        100000
    )

    return salt + key


def verify_passwd(pwd, old_hash):
    """
    utility func to verify that given passwd is correct
    :param pwd:
    :param old_hash:
    :return: Bool
    """
    from hashlib import pbkdf2_hmac as hasher
    salt = old_hash[:64]
    key_old = old_hash[64:]

    key_new = hasher(
        'sha256',
        pwd.encode('utf-8'),
        salt,
        100000
    )
    return key_new == key_old


def change_passwd(old_pwd, new_pwd, old_pwd_in, user_obj):
    """
    utility func to change a pwd of a new user
    :param user_obj: user object for passwd change
    :param old_pwd_in: :type:str
    :param old_pwd: :type:bString
    :param new_pwd: :type:str
    :return: tuple
    """
    if verify_passwd(old_pwd_in, old_pwd):
        user_obj.passwd = hash_passwd(new_pwd)
        return 1, user_obj
    else:
        return 0, "The old password is incorrect"


def subscribe_group(user, group_obj):
    """
    utility func to subscribe a user(s) to a group
    :param user: int
    :param group_obj: group obj for subscription
    :return: tuple
    """
    try:
        # from mongo.collection_group_user.CREATE import create TODO: check this
        pass
    except Exception as e:
        return 0, e.__str__()
    else:
        return 1, group_obj


def unsubscribe_group(user, group_obj):
    """
    utility func to unsubcribe a user from a group
    :param user: int
    :param group_obj: group obj for unsubscription
    :return: tuple
    """
    try:
        index = group_obj.members.indexof(user)
        group_obj.members.pop(index)
    except Exception as e:
        return 0, e.__str__()
    else:
        return 1, group_obj
