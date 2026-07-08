class RDMOException(Exception):
    pass


class MailSendError(RDMOException):
    def __init__(self, reason, original_exception=None):
        super().__init__(reason)
        self.reason = reason
        self.original_exception = original_exception
