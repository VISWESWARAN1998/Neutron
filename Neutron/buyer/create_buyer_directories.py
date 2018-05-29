# SWAMI KARUPPASWAMI THUNNAI

import os


# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# create_buyer_directories.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 23-05-2018


def create_buyer_directories(buyer_id):
    """
    This will create all the necessary directories for a
    particular buyer id
    :param buyer_id: The id of the particular buyer
    :return: None
    """
    dir_list = [
        "neutron_static/buyer/"+str(buyer_id)
    ]
    for directory in dir_list:
        os.makedirs(directory)


