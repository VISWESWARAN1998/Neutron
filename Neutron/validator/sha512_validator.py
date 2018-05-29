# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# sha512_validator.py - Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 24.05.2018

import string


def is_valid_sha512_hash(sha512_hash):
    """
    This method will check if the entered string is a valid
    SHA512 hash.
    :param sha512_hash:
    :return: True if it is a valid SHA512 hash
    """
    if len(sha512_hash) == 128:
        valid_hash_chars = list(string.ascii_lowercase+string.digits)
        for character in sha512_hash:
            if not character in valid_hash_chars:
                return False
        return True
    return False