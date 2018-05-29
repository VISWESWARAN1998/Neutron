# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# id_not_found.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 23-05-2018


class IDNotFoundException(Exception):
    """
    This excpetion will be thrown if the buyer/seller/admin id is
    not present in the database but requested.
    """
    pass