import hashlib


def compute_checksum(string):
    return hashlib.sha1(string).hexdigest()
