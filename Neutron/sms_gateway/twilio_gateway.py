# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# twilio_gateway.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 29-05-2018

import json
from twilio.rest import Client


class TwilioGateway:

    @staticmethod
    def send_sms(phone_no, body):
        """
        Send sms to the desired phone no
        :param phone_no: The phone_no to which the message is about to be sent
        :param body: The body of the message
        :return: True if the sms is sent else will return False
        """
        try:
            with open("twilio_credential.json") as json_file:
                credentials = json.load(json_file)
                client = Client(credentials["account_sid"], credentials["auth_token"])
                client.messages.create(
                    body=body,
                    from_=credentials["phone"],
                    to=phone_no
                )
                print("sent")
                return True
        except Exception as e:
            print(e)
            return False
        return False
