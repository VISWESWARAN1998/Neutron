# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# name.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 23-05-2018

import string


def is_name_valid(name, size=50, additional_chars=None):
    """
    Checks whether the input string is a person name or not
    :param name: The name of the person
    :param size: The size to be validated
    :param additional_chars: This is a special case. additional_chars will be list, the characters
    present in the list will be considered as valid. This is an optional argument
    :return: True if the string is a valid person name
    """
    if len(name) > size:
        return False
    alphabets = list(string.ascii_lowercase)
    if additional_chars:
        alphabets.extend(additional_chars)
    name = name.lower()
    for i in name:
        if not i in alphabets:
            return False
    return True