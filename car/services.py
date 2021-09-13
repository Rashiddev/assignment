import hashlib
import time


def generate_hash():
    hash_field = hashlib.sha1()
    hash_field.update(str(time.time()).encode())
    # return hash_field.hexdigest()[:33]
    return hash_field.hexdigest()
