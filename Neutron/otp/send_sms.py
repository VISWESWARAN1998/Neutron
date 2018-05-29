# SWAMI KARUPPASWAMI THUNNAI


# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# send_sms.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 29-05-2018


import time

from exceptions.id_not_found import IDNotFoundException
from exceptions.no_such_gateway import NoSuchGateWayException
from otp.genrate_otp import GenerateOTP
from sms_gateway.twilio_gateway import TwilioGateway


class SendSMS:
    def __init__(self, id, account_type, connection):
        """
        Constructor to initialize the instance variables
        :param id: Buyer id / Seller id
        :param account_type: Either buyer or seller
        :param connection: PyMySQL connection object for MySQL database
        """
        self.__id = id
        self.__available_gateways = ("twilio", )
        self.__gateway = None
        self.__account_type = account_type
        self.__connection = connection
        self.__country_code = "+91"


    @property
    def gateway(self):
        return self.__gateway

    @gateway.setter
    def gateway(self, gateway_name):
        """
        Setter to set the gateway name
        :param gateway_name: The name of the SMS gateway
        :return: None
        :raises NoSuchGateWayException
        """
        gateway_name = gateway_name.lower()
        if gateway_name in self.__available_gateways:
            self.__gateway = gateway_name
        else:
            raise NoSuchGateWayException

    def send(self):
        cursor = self.__connection.cursor()
        if self.__account_type == "buyer":
            cursor.execute("select phone_no from neutron_buyer where buyer_id=%s", (self.__id,))
        result = cursor.fetchone()
        if result:
            phone_number = self.__country_code + result["phone_no"]
            otp = GenerateOTP.new_otp()
            creation_time = time.time()
            if self.__account_type == "buyer":
                cursor.execute(
                    "insert into otp value(%s, 0, %s, %s)",
                    (result["phone_no"], otp, creation_time)
                )
                self.__connection.commit()
            if self.__gateway == "twilio":
                if TwilioGateway.send_sms(phone_number, "Neutron Verification code is "+ str(otp)+". Happy Shopping!"):
                    return True
                return False
        else:
            raise IDNotFoundException

