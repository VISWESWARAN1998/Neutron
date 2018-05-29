# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIAVM
# invalid_arguments.py - Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 19-05-2018

def is_invalid_arguments_present(*args):
    """
    This method will make sure that all the arguments are present in the query
    sent to flask-api. If any of the parameter is None then it will return True.

    Note: This method WILL RETURN TRUE FOR MALICIOUS INPUTS.

    :param args: The arguments passed to the flask query
    :return: True if some or all arguments is missing else False
    """
    if None in args:
        return True
    return False
