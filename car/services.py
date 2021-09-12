import hashlib
import time


def generate_hash():
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode())
    return hash.hexdigest()[:33]