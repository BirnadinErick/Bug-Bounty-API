#      Author: Birnadin Erick
#      Copyright © 2021. All rights are reserved by Birnadin Erick.
#      This script can be used without any written acknowledgement from author for personal or commercial purpose.
#
class MyException(Exception):
    """
    Base Exception for my custom exceptions
    """
    pass


class UseAsModule(MyException):

    def __init__(self):
        self.msg = "This file should be used as a module, not to be run independently"
        super().__init__(self.msg)
