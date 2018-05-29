# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# sign_up.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 22-05-2018

import time
import json
import jwt

class BuyerLogin:
    """
    This class will yeild JSON Web Token for the particular buyer
    who performs the login operation successfully.
    """
    __phone_number = None
    __sha512_hash = None
    __connection = None

    def __init__(self, phone_number, sha512_hash, connection):
        """
        Constructor to initialize the instance variables
        :param phone_number: The phone number
        :param sha512_hash: The hash of the password
        :param connection: PyMySQL connection object for MySQL database.
        """
        self.__phone_number = phone_number
        self.__sha512_hash = sha512_hash
        self.__connection = connection

    def login(self):
        """
        :return: Will return JWT
        """
        cursor = self.__connection.cursor()
        cursor.execute(
            "select * from neutron_buyer_credential where phone_no=%s and password=%s",
            (self.__phone_number, self.__sha512_hash)
        )
        result = cursor.fetchone()
        if result is None:
            return None
        cursor.execute("select buyer_id from neutron_buyer where phone_no=%s", (self.__phone_number))
        id = cursor.fetchone()
        if id is None:
            return None
        buyer_id = id["buyer_id"]
        expiry = self.__get_expiry_time()
        buyer_secret = self.__get_buyer_credential() + self.__sha512_hash
        token = self.__generate_buyer_token(buyer_id=buyer_id, buyer_secret=buyer_secret, expiry=expiry)
        return token

    def __get_expiry_time(self):
        """
        This will get the expiry time of a JWT token which is excatly
        3 days from the current time.
        :return: 3 days from now in seconds
        """
        current_time = time.time()
        after_three_days = current_time + 259200
        return after_three_days

    def __get_buyer_credential(self):
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

    def __generate_buyer_token(self, buyer_id, expiry, buyer_secret):
        """
        Will generate the json web token with the help of the credentials
        :param buyer_id: The id of the buyer
        :param expiry: The expiry date which is usually 3 days
        :param buyer_secret: The buyer secret which is used to encrypt the JWT.
        :return: JWT for the particular buyer
        """
        token = jwt.encode(
            {
                "buyer_id": buyer_id,
                "expiry" : expiry
            },
            buyer_secret
        )
        return token.decode("utf-8")



