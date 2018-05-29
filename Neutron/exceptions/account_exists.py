# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# account_exists.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 19-05-2018

class AccountExistsException(Exception):
    """
    This class is used to throw a custom exception which is used
    to prevent creating multiple accounts using same phone number.
    """
    pass