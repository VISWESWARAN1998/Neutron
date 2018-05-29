# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# token_validator.py - Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 25.05.2018

import jwt
import time
from buyer.buyer_credential import get_buyer_credential
from exceptions.token_expired import TokenExpiredException


class BuyerTokenValidator:
    """
    This class is used to validate the buyer token. This will provide access only to
    the authorized user.
    """
    def __init__(self, token, connection):
        """
        Constructor to initialize the instance variables
        :param token: The buyer token
        :param connection: PyMySQL connection object
        """
        self.__token = token
        self.__connection = connection
        self.__message = None
        self.__buyer_id = None

    def is_token_valid(self):
        """
        This method will validate the token
        :return: True if the token is valid else False
        :raises: TokenExpiredException
        """
        try:
            token_details = jwt.decode(self.__token, verify=False)
            buyer_id = token_details["buyer_id"]
            self.__buyer_id = buyer_id
            expiry = token_details["expiry"]
            if time.time() > expiry:
                raise TokenExpiredException
            int(buyer_id)
            cursor = self.__connection.cursor()
            cursor.execute("select phone_no from neutron_buyer where buyer_id=%s", (buyer_id,))
            result = cursor.fetchone()
            if result is None:
                self.__message = "Account not exists"
                return False
            phone_number = result["phone_no"]
            cursor.execute("select password from neutron_buyer_credential where phone_no=%s", (phone_number,))
            result = cursor.fetchone()
            if result is None:
                self.__message = "Account not exists"
                return False
            password = result["password"]
            buyer_secret = get_buyer_credential() + password
            if jwt.decode(self.__token, key=buyer_secret, verify=True):
                return True
            return False
        except jwt.DecodeError:
            self.__message = "Invalid Token"
            return False
        except KeyError:
            self.__message = "Insecure Token"
            return False
        except ValueError:
            self.__message = "Insecure Token"

    def get_buyer_id(self):
        """
        This method is used to get the buyer id from the JWT token
        :return: buyer_id from the token
        """
        return self.__buyer_id

    def __str__(self):
        return str(self.__message)
