# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# buyer_credential.py - Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 25.05.2018


import json


def get_buyer_credential():
    """
    This method is used to get the buyer credential from
    neutron_credentials.json file which will be used as a
    partial secret key for the json web token.
    :return: buyer secret key
    """
    buyer_secret = None
    with open("neutron_credentials.json", "r") as credentails:
        all_credentials = json.load(credentails)
        buyer_secret = all_credentials["buyer_secret"]
    return buyer_secret