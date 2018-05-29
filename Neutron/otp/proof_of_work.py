# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# proof_of_work.py Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 22-05-2018


import random
import string
import hashlib


class ProofOfWork:
    """
    Proof of Work needs to send along with the OTP for checking.
    It will increase the brute-forcing time.

    Hash cracked: 1 in 5040 should be the correct value
    """
    @staticmethod
    def new_proof_of_work():
        answer = ""
        sha512 = None
        while len(answer) != 5:
            value = random.choice(string.digits+string.ascii_lowercase)
            if not value in answer:
                answer+=value
        sha512 = hashlib.sha512(answer.encode("utf-8")).hexdigest()
        return answer, sha512