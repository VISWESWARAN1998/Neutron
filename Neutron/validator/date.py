# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# date.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 23-05-2018

import datetime

def is_date_valid(date):
    """
    Checks whether the date is in a valid mysql format
    :param date: The date to be validated
    :return: True if the format supports the mysql date datatype
    """
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False