class MyException(Exception):
    """
    Base Exception for my custom exceptions
    """
    pass


class UseAsModule(MyException):

    def __init__(self):
        self.msg = "This file should be used as a module, not to be run independently"
        super().__init__(self.msg)
