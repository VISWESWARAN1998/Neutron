# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# add_address.py - Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 27.05.2018

import base64


class AddBuyerAddress:
    """
    This class is used to add the address of the buyer.
    """

    def __init__(self, buyer_id, address_line_one, address_line_two,
                 city_id, pincode, latitude, longitude, connection):
        """
        Constructor to initialize the instance variables
        :param buyer_id: The id of the buyer
        :param address_line_one: The address line one of the buyer
        :param address_line_two: The address line two of the buyer
        :param city_id: The city id of the buyer
        :param pincode: The pincode of the buyer
        :param latitude: The latitude of the buyer
        :param longitude: The longitude of the buyer
        :param connection: PyMySQL connection object
        """
        self.__buyer_id = buyer_id
        self.__address_line_one = base64.b64decode(address_line_one).decode("utf-8")
        self.__address_line_two = base64.b64decode(address_line_two).decode("utf-8")
        self.__city_id = city_id
        self.__pincode = pincode
        self.__latitude = latitude
        self.__longitude = longitude
        self.__connection = connection

    def add_address(self):
        """
        Add the address to the MYSQL database
        :return: True if the address is added else false
        """
        try:
            cursor = self.__connection.cursor()
            cursor.execute(
                "insert into neutron_buyer_address value(null, %s, %s, %s, %s, %s, %s, %s)",
                (
                    self.__buyer_id, self.__address_line_one, self.__address_line_two,
                    self.__city_id, self.__pincode, self.__latitude, self.__longitude
                 )
            )
            self.__connection.commit()
            return True
        except:
            return False
