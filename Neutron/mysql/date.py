# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# date.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 22-05-2018


import datetime


def date():
    """
    Used to get the current date in the format which supports
    the 'date' data-type of MySQL Database.
    :return: The current data in this format: YYYY-MM-DD e.g '2018-05-22'
    """
    current_date = str(datetime.datetime.now().date())
    return current_date