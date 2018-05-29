# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# get_admin_credential.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 26-05-2018

import json


def get_admin_credential():
    # admin_credential = None
    with open("neutron_credentials.json", "r") as json_file:
        content = json.load(json_file)
        admin_credential = content["admin_secret"]
    return admin_credential