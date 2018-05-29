# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# base_64.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 27-05-2018

import base64
import binascii


def is_valid_base64(string):
    """
    This function will return True if the string is a valid base64
    :param string: The string which is to be checked
    :return: True if the string is a valid base64 string
    else will return False
    """
    try:
        base64.b64decode(string)
        return True
    except binascii.Error:
        return False