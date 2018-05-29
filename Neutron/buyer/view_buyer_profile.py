# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# neutron.py - Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 27.05.2018

from exceptions.id_not_found import IDNotFoundException


class ViewBuyerProfile:
    """
    This class is used to view the public details of the buyer like
    1. First Name
    2. Middle Name
    3. Last Name
    4. Buyer ID
    5. Total Products purchased
    """


    def __init__(self, buyer_id, connection):
        self.__buyer_id = buyer_id
        self.__connection = connection

    def get_profile_details(self):
        """
        This method is used to get the buyer's public profile details.
        :return: Buyer's public profile.
        :raises: IDNotFoundException if the buyer id is not found in the database
        """
        cursor = self.__connection.cursor()
        cursor.execute(
            "select first_name, last_name, purchased_products from neutron_buyer where buyer_id=%s",
            (self.__buyer_id,)
        )
        result = cursor.fetchone()
        if result:
            return result
        raise IDNotFoundException
