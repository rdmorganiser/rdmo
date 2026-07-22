from smtplib import SMTPException


class RDMOException(Exception):
    pass

class SendMailException(SMTPException):
    pass
