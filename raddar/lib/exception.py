class RaddarException(Exception):
    pass


class FailedToCloneRepoException(RaddarException):
    pass


class FailedToWriteRepoException(RaddarException):
    pass
