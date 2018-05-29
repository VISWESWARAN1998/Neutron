# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# detail.py - Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 25.05.2018


class BuyerDetail:

    def __init__(self, buyer_id, connection):
        self.__buyer_id = buyer_id
        self.__connection = connection

    def get_buyer_details(self):
        """
        This method is used to get the buyer details
        :return: The details of the buyer will be returned as a dict object
        in Python. None if not found
        """
        try:
            cursor = self.__connection.cursor()
            cursor.execute("select * from neutron_buyer where buyer_id=%s", (self.__buyer_id,))
            result = cursor.fetchone()
            print(result)
            if result:
                return result
        except Exception as e:
            print(e)
            return None
        return None