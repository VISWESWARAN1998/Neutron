# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# generate_otp.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 20-05-2018

import random

class GenerateOTP:
    """
    This class is used for OTP genration.
    """

    @staticmethod
    def new_otp():
        """
        Will generate a new 5 digit random OTP

        Probability of finding this random number:
        10 * 10 * 10 * 10 * 10 = 100000 i.e 1 in a lakh combination is required
        :return:
        """
        random_number = random.randrange(10000, 99999)
        return random_number