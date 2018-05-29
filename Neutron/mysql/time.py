# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# time.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 22-05-201

import datetime


def time():
    """
    :return: Will return the current time in the format which supports
    the MySQL data-type 'time'
    """
    current_time = str(datetime.datetime.now().time())
    current_time = current_time.split(".")
    return current_time[0]