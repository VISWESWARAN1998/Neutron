# SWAMI KARUPPASWAMI THUNNAI


def is_city_id_valid(connection, city_id):
    """
    This function will check whether the city id is a valid one or not
    :param connection: PyMySQL connection object for mysql database
    :param city_id: The id of the city
    :return: True if the city id is valid else it will return False
    """
    try:
        city_id = int(city_id)
        cursor = connection.cursor()
        cursor.execute("select * from city where city_id=%s", (city_id) )
        result = cursor.fetchone()
        if result:
            return True
        return False
    except ValueError:
        return False

