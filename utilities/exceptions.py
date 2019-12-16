class RootException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super(BaseException, self).__init__(*args, **kwargs)


class ResourceExists(RootException):
    pass


class ResourceDoesNotExist(RootException):
    pass
