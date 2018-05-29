# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# sign_up.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 19-05-2018


from exceptions.account_exists import AccountExistsException

class SellerSignUp:
    """
    This class will create a new seller account.

    MySQL tables altered:
    ---------------------
    SELECT AND INSERT:
        1. neutron_seller_credential
        2. neutron_seller_account_detail
    """

    def __init__(self, phone_number, sha512_hash, connection):
        """
        Constructor to initialize the instance variables

        :param phone_number: The phone number of the seller
        :param sha512_hash: The password of the sha512 hash
        :param connection: The pymysql connection object for MySQL database.
        """
        self.__phone_number = phone_number
        self.__sha512_hash = sha512_hash
        self.__connection = connection

    def create_account(self):
        """
        This method will create a new seller account.
        :return: True if the account is created else False.
        :raises: AccountExistsException
        """
        pass


