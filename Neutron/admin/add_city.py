# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# add_city.py - Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 26.05.2018


def add_city(connection, city_name, state):
    """
    This function is used to add new city and this is an admin
    only function.
    :param connection: PyMySQL connection object
    :param city_name: The name of the city
    :param state: The state of the city
    :return: None
    """
    city_name = city_name.lower()
    city_name = city_name.capitalize()
    state = state.lower()
    state = state.capitalize()
    cursor = connection.cursor()
    cursor.execute("select city, state from city where city=%s and state=%s"
                   , (city_name, state))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("insert into city value(null, %s, %s)", (city_name, state))
        connection.commit()
        return True
    else:
        return False

