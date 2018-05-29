# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# token_validator.py - Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 26.05.2018

import jwt
import time
from exceptions.token_expired import TokenExpiredException
from admin.get_admin_credential import get_admin_credential

class AdminTokenValidator:
    """
    This class is used to validate the admin token. This will provide access only to
    the authorized admin.
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
        self.__admin_id = None
        self.__username = None

    def is_token_valid(self):
        """
        This method will validate the token
        :return: True if the token is valid else False
        :raises: TokenExpiredException
        """
        try:
            token_details = jwt.decode(self.__token, verify=False)
            self.__admin_id = token_details["id"]
            self.__username = token_details["username"]
            expiry = token_details["expiry"]
            if time.time() > expiry:
                raise TokenExpiredException
            cursor = self.__connection.cursor()
            cursor.execute(
                "select password from neutron_admin_credential where admin_id=%s and username=%s",
                (self.__admin_id, self.__username)
            )
            result = cursor.fetchone()
            if result is None:
                self.__message = "Invalid id details"
                return False
            passsword = result["password"]
            admin_secret =  passsword + get_admin_credential()
            jwt.decode(self.__token, key=admin_secret, verify=True)
            return True
        except jwt.DecodeError:
            self.__message = "Invalid Token"
            return False
        except KeyError:
            self.__message = "Insecure Token"
            return False
        except ValueError:
            self.__message = "Insecure Token"

    def __str__(self):
        return str(self.__message)
