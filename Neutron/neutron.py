# SWAMI KARUPPASWAMI THUNNAI

# PROJECT NEUTRON
# COPYRIGHT(C) 2018 - VISWESWARAN NAGASIVAM
# neutron.py - Written by, Visweswaran Nagasivam
# Contact: visweswaran.nagasivam98@gmail.com
# Date: 19.05.2018

from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask_restful import Api
from flask_restful import Resource
from flask import render_template
from flask import redirect
from flask import url_for
import json
import jwt
import string
import base64
from otp.send_sms import SendSMS
"""MySQL related imports"""
import pymysql
"""Custom exceptions"""
from exceptions.account_exists import AccountExistsException
from exceptions.token_expired import TokenExpiredException
from exceptions.incorrect_password import IncorrectPasswordException
from exceptions.id_not_found import IDNotFoundException
"""Security related imports"""
from validator.invalid_arguments import is_invalid_arguments_present
from validator.phone_no import is_valid_phone_number
from validator.name import is_name_valid
from validator.date import is_date_valid
from validator.sha512_validator import is_valid_sha512_hash
from validator.city_id import is_city_id_valid
from validator.base_64 import is_valid_base64
"""Buyer related imports"""
from buyer.sign_up import BuyerSignUp
from buyer.log_in import BuyerLogin
from buyer.token_validator import BuyerTokenValidator
from buyer.detail import BuyerDetail
from buyer.add_address import AddBuyerAddress
from buyer.view_buyer_profile import ViewBuyerProfile
"""Admin related imports"""
from admin.login import AdminLogin
from admin.token_validator import AdminTokenValidator
from admin.add_city import add_city

connection = pymysql.connect(
    host="127.0.0.1",
    user="visweswaran",
    password="visweswaran",
    db="neutron",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
api = Api(app)


############################################################
#                   CONSTANTS
############################################################

INSECURE_PARAMETER = "Neutron Validator: Insecure param found"
INSUFFICIENT_PARAMETER = "Neutron Validator: Insufficient args found"
EXPIRED_TOKEN = "Neutron Validator: Token has been expired"
INVALID_CREDENTIALS = "Neutron Validator: Invalid credentials"

##################################################################


@app.route("/")
def main():
    return render_template("not_permitted.html")


class NeutronVersion(Resource):
    def get(self):
        content = None
        with open("version.json", "r") as json_file:
            content = json.load(json_file)
        return jsonify(content)


# ###############################################################
# BELOW IS THE NECESSARY METHODS FOR ADMIN
# ##############################################################


def admin_only(flask_method):
    def wrapper_function(*args):
        if request.method == "POST":
            token = request.form["token"]
            token_validator = AdminTokenValidator(
                token=token, connection=connection)
            try:
                if not token_validator.is_token_valid():
                    error_message = str(token_validator)
                    abort(400, error_message)
            except TokenExpiredException:
                abort(400, EXPIRED_TOKEN)
            return flask_method(*args)

    return wrapper_function


class NeutronAdminLogin(Resource):
    def post(self):
        username = request.form["username"]
        password = request.form["password"]
        if not is_valid_sha512_hash(password):
            abort(400, INSECURE_PARAMETER + "-password")
        valid_user_name_chars = list(string.ascii_lowercase + string.digits)
        for i in username:
            if not i in valid_user_name_chars:
                abort(400, INSECURE_PARAMETER + "-username")
        try:
            token = AdminLogin(
                connection=connection, username=username, password=password)
            result = token.login()
            if result:
                return jsonify({"token": result})
            else:
                abort(400, INVALID_CREDENTIALS)
        except IncorrectPasswordException:
            abort(400, INVALID_CREDENTIALS)


class NeutronAdminAddCity(Resource):
    @admin_only
    def post(self):
        city = request.form["city"]
        state = request.form["state"]
        if not is_name_valid(city, size=100, additional_chars=[".", " "]):
            abort(400, "Neutron Validator: Insecre city name found")
        if not is_name_valid(state, size=100):
            abort(400, "Neutron Validator: Insecre state name found")
        if add_city(connection=connection, city_name=city, state=state):
            return jsonify({"message": "City added"})
        else:
            return jsonify({"message": "City exists already"})


# ###############################################################
# BELOW IS THE NECESSARY METHODS FOR BUYER
# ##############################################################


def registered_buyer_only(flask_restful_method):
    def wrapper_function(*arguments):
        # Check which type of method
        if request.method == "GET":
            token = request.args.get("token")
            if is_invalid_arguments_present(token):
                abort(400, "Neutron: Not logged in")
        elif request.method == "POST":
            token = request.form["token"]
        else:
            abort(400, "Unsupported method")
        ####################################
        if is_invalid_arguments_present(token):
            abort(
                400,
                "Neutron Validator: Insufficient args to satisfy the request"
            )
        error_message = None
        token_validator = BuyerTokenValidator(token, connection)
        try:
            if not token_validator.is_token_valid():
                error_message = str(token_validator)
                abort(401, error_message) # HTTP STATUS CODE 401 - Unauthorized
        except TokenExpiredException:
            abort(400, "Login was expired. Please login once again.")

        return flask_restful_method(*arguments)

    return wrapper_function


class NeutronBuyerLogin(Resource):
    """
    API FOR BUYER LOGIN

    Methods Supported: POST ONLY

    :returns: JWT login token for the specifc buyer if something is wrong
    appropirate error message will be returned.
    """

    def post(self):
        phone_number = request.form["phone"]
        password_hash = request.form["hash"]
        if is_invalid_arguments_present(phone_number, password_hash):
            abort(
                400,
                INSUFFICIENT_PARAMETER
            )
        if not is_valid_phone_number(phone_number):
            abort(400, INSECURE_PARAMETER + "-phone_number")
        login = BuyerLogin(
            phone_number=phone_number,
            sha512_hash=password_hash,
            connection=connection)
        try:
            token = login.login()
            if token:
                return jsonify({"token": token})
            else:
                abort(400, "Neutron Validator: Invalid credentials.")
        except IncorrectPasswordException:
            abort(400, "Neutron Validator: Invalid credentials.")


class BuyerSignUpAPI(Resource):
    """
    This class is used to create a new buyer account.
    In order to create a buyer account one must require
    --------------------------------------------------
    1. Valid Phone number
    2. First Name
    3. Middle Name(if any)
    4. Last Name
    5. Date of Birth (We need to know whether our customer is a child or an adult)
    6. SHA512 hash of their password, this will be done from the application side.
    """

    def post(self):
        phone = request.form["phone"]
        sha512_hash = request.form["hash"]
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        dob = request.form["dob"]
        if middle_name is "":
            middle_name = None
        if is_invalid_arguments_present(phone, sha512_hash, first_name,
                                        last_name, dob):
            abort(
                400,
                "Neutron Validator: Insufficient params to perform this operation."
            )
        if not is_valid_phone_number(phone):
            abort(400, "Neutron Validator: Insecure Phone number found.")
        if not is_name_valid(first_name):
            abort(400, "Neutron Validator: Insecure param first name found.")
        if not is_name_valid(last_name):
            abort(400, "Neutron Validator: Insecure param last name found.")
        if middle_name:
            if not is_name_valid(middle_name):
                abort(400,
                      "Neutron Validator: Insecure param middle name found.")
        if not is_date_valid(dob):
            abort(400, "Neutron Validator: Insecure param date found.")
        # If everything is OK then 200 status code should be returned
        account_created = False
        message = "Reason Unknown. Please try again :)"
        sign_up = BuyerSignUp(
            phone_number=phone,
            password_hash=sha512_hash,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            dob=dob,
            connection=connection)
        try:
            if sign_up.sign_up():
                account_created = True
                message = "Account has been created"
        except AccountExistsException:
            message = "Account already exists"

        return jsonify({
            "account_created": account_created,
            "message": message
        })


class NeutronBuyerDetail(Resource):
    """
    This class will return the requested buyer detail if valid
    auth token is provided.
    """

    @registered_buyer_only
    def get(self):
        token = request.args.get("token")
        token_content = jwt.decode(token, verify=False)
        buyer_detail = BuyerDetail(
            buyer_id=token_content["buyer_id"], connection=connection)
        if buyer_detail.get_buyer_details():
            return jsonify(buyer_detail.get_buyer_details())
        abort(400,
              "Neutron Validator: Buyer details does not seems to be exist.")


class NeutronBuyerAddAddress(Resource):
    """
    This class is used to add the buyer address
    """
    @registered_buyer_only
    def post(self):
        token = request.form["token"]
        token_content = jwt.decode(token, verify=False)
        buyer_id = token_content["buyer_id"]
        city_id = request.form["city_id"]
        adddress_line_one = request.form["addr1"]
        adddress_line_two = request.form["addr2"]
        pincode = request.form["pin"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        if not is_city_id_valid(connection=connection, city_id=city_id):
            abort(400, "Neutron Validator: City not found")
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            abort(400, "Neutron Validator: Invalid latitude and longitude details")
        if not is_valid_base64(adddress_line_one):
            abort(400, "Neutron Validator: Invalid address format")
        if not is_valid_base64(adddress_line_two):
            abort(400, "Neutron Validator: Invalid address format")
        try:
            pincode = int(pincode)
        except ValueError:
            abort(400, "Neutron Validator: Invalid Pincode format")
        length_of_address_one = len(base64.b64decode(adddress_line_one))
        if length_of_address_one > 1000:
            abort(400, "Neutron Validator: Address length too long")
        length_of_address_two = len(base64.b64decode(adddress_line_two))
        if length_of_address_two > 1000:
            abort(400, "Neutron Validator: Address length too long")
        address = AddBuyerAddress(
            buyer_id=buyer_id, address_line_one=adddress_line_one, address_line_two=adddress_line_two,
            city_id=city_id, pincode=pincode, latitude=latitude, longitude=longitude, connection=connection
        )
        if address.add_address():
            return jsonify({"message": "Address has been added"})
        else:
            return jsonify({"message": "Address cannot be added"})


class NeutronBuyerProfile(Resource):
    @registered_buyer_only
    def get(self):
        buyer_id = request.args.get("id")
        if is_invalid_arguments_present(buyer_id):
            abort(400, INSUFFICIENT_PARAMETER)
        try:
            buyer_id = int(buyer_id)
            try:
                profile = ViewBuyerProfile(buyer_id=buyer_id, connection=connection)
                return jsonify(profile.get_profile_details())
            except IDNotFoundException:
                abort(400, "Invalid buyer id")
        except ValueError:
            abort(400, INSECURE_PARAMETER)


class NeutronBuyerVerifyPhone(Resource):
    @registered_buyer_only
    def post(self):
        token = request.form["token"]
        contents = jwt.decode(token, verify=False)
        buyer_id = contents["buyer_id"]
        sms = SendSMS(buyer_id, "buyer", connection)
        sms.gateway = "twilio"
        if sms.send():
            return jsonify({"message": "Sms has been sent"})
        else:
            abort(400, "Sms not sent due to some problem. Please check the phone number")



####################################################################################



##################################################################################
#           CUSTOM ERROR TEMPLATES
##################################################################################
@app.errorhandler(404)
def handler(e):
    return redirect("/")
##################################################################################
api.add_resource(NeutronVersion, "/version")
"""
ADMIN RELATED RESOURCES
"""
api.add_resource(NeutronAdminLogin, "/neutronAdmin/login")
api.add_resource(NeutronAdminAddCity, "/neutronAdmin/addCity")
"""
BUYER RELATED RESOURCES
"""
api.add_resource(BuyerSignUpAPI, "/buyer/sign_up")
api.add_resource(NeutronBuyerLogin, "/buyer/login")
api.add_resource(NeutronBuyerDetail, "/buyer/info")
api.add_resource(NeutronBuyerAddAddress, "/buyer/add_address")
api.add_resource(NeutronBuyerProfile, "/buyer/profile")
api.add_resource(NeutronBuyerVerifyPhone, "/buyer/verify")

if __name__ == "__main__":
    app.run(debug=True)