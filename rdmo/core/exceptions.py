class RDMOException(Exception):
    pass


class MailSendError(Exception):
    def __init__(self, reason, original_exception=None):
        super().__init__(reason)
        self.reason = reason
