# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# login.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 26-05-2018

from admin.get_admin_credential import get_admin_credential
import time
import jwt
from exceptions.incorrect_password import IncorrectPasswordException

class AdminLogin:
    """
    This class is used by administrators for logging into
    the web-service.
    """

    def __init__(self, connection, username, password):
        """
        Constructor to initialize the values.
        :param connection: PyMySQL connection object
        :param username: The username of the administrator
        :param password: The password of the administrator
        """
        self.__connection = connection
        self.__username = username
        self.__password = password

    def login(self):
        """
        This is used for logging into administrators account
        :return: token if the password and username is correct.
        :raises: IncorrectPasswordException
        """
        cursor = self.__connection.cursor()
        cursor.execute(
            "select * from neutron_admin_credential where username=%s and password=%s",
            (self.__username, self.__password)
        )
        result = cursor.fetchone()
        if result is None:
            raise IncorrectPasswordException
        admin_id = result["admin_id"]
        username = result["username"]
        password = result["password"]
        admin_partial_secret = get_admin_credential()
        admin_secret = password + admin_partial_secret
        expiry = self.get_expiry_time()
        token = jwt.encode({"username": username, "id": admin_id, "expiry": expiry}, admin_secret)
        return token

    def get_expiry_time(self):
        """
        This will get the expiry time of a JWT token which is excatly
        7 days from the current time.
        :return: 7 days from now in seconds
        """
        current_time = time.time()
        after_three_days = current_time + 604800
        return after_three_days

