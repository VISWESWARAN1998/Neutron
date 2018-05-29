# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# sign_up.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 19-05-2018


import pymysql
from exceptions.account_exists import AccountExistsException
from buyer.create_buyer_directories import create_buyer_directories
from mysql.date import date
from mysql.time import time


class BuyerSignUp:
    """
    This class is used to create a new buyer account
    """

    def __init__(self, phone_number, password_hash, first_name, middle_name, last_name, dob, connection):
        """
        Constructor to initialize the instance variables.

        :param phone_number: The phone number of the buyer
        :param password_hash: The sha512 hash of the password of the buyer
        :param first_name: First Name of the buyer
        :param last_name: Last Name of the buyer
        :param middle_name: Middle Name of the buyer
        :param dob: Date of Birth of the buyer
        :param connection: PyMySQL connection object for the MySQL database
        """
        self.__phone_number = phone_number
        self.__password_hash = password_hash
        self.__connection = connection
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__last_name = last_name
        self.__dob = dob

    def sign_up(self):
        """
        This method is used to create a new buyer account
        :return:
        """
        try:
            cursor = self.__connection.cursor()
            cursor.execute(
                "insert into neutron_buyer_credential values(%s, %s)",
                (self.__phone_number, self.__password_hash)
            )
            current_date = date()
            current_time = time()
            cursor.execute(
                "insert into neutron_buyer_account values (%s, %s, %s, 0)",
                (self.__phone_number, current_date, current_time)
            )
            cursor.execute(
                "insert into neutron_buyer values(null, %s, %s, %s, %s, %s, 0)",
                (self.__phone_number, self.__first_name, self.__middle_name, self.__last_name, self.__dob)
            )
            buyer_id = cursor.lastrowid
            create_buyer_directories(buyer_id=buyer_id)
            self.__connection.commit()
            return True
        except pymysql.IntegrityError:
            raise AccountExistsException
        return False