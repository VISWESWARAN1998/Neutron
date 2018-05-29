# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# phone_no.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 19-05-2018

import string

def is_valid_phone_number(phone_number):
    """
    Validates whether a phone no is a valid one or not

    Args:
        phone_number: The phone number which is
        to be validated
    Returns:
        True if the phone number is valid else 
        will return False
    """
    # Indian Phone no have length of 10 for other countries
    # please change the length
    if not len(phone_number) is 10:
        return False
    valid_number_list = list(string.digits)
    for number in phone_number:
        if not number in valid_number_list:
            return False
    return True

