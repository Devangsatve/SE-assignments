
from dotenv import load_dotenv, find_dotenv
from io import StringIO
from os import environ as env
from Python_otp import OTPService
import sys
import unittest
from unittest.mock import patch
load_dotenv(find_dotenv())

EMAIL = env.get('EMAIL')
EMAIL_PASSWD = env.get('PASSWORD')
LENGTH = int(env.get("OTP_LENGTH"))

class TestOTPService(unittest.TestCase):

    def setUp(self):
        self.otpService = OTPService(EMAIL, EMAIL_PASSWD)
        self.otpService.initiateServer()

    def tearDown(self):
        self.otpService.closeServer()

    def test_generateOTP(self):
        print("\n\t----------Testing For generateOTP----------\n")

        len1 = 5
        len2 = 3

        # First, _OTP is initialized Empty
        self.assertEqual(self.otpService._OTP, "")

        # Generation OTP
        self.otpService.generateOTP(len1)
        self.assertEqual(len(self.otpService._OTP), len1)

        # Generating with err -> length as 3
        self.assertEqual(self.otpService.generateOTP(len2), False)

    def test_sendMail(self):
        print("\n\t----------Testing For sendMail---------\n")

        email1 = "" # Enter email for test
        email2 = "" # Enter different email for test

        expected_output = "\n\tOTP is sent to the given email address\n"

        with patch('sys.stdout', new = StringIO()) as output:
            self.otpService.generateOTP(6)
            self.otpService.sendMail(email1)
            self.assertEqual(output.getvalue(), expected_output)

        with patch('sys.stdout', new = StringIO()) as output:
            self.otpService.generateOTP(6)
            self.otpService.sendMail(email2)
            self.assertEqual(output.getvalue(), expected_output)
    
    def test_validateOTP(self):
        print("\n\t----------Testing For validateOTP----------\n")

        with patch('sys.stdout', new = StringIO()) as output:
            self.otpService.generateOTP(5)
            self.otpService.validateOTP(self.otpService._OTP)
            self.assertEqual(output.getvalue(), "Given OTP was correct\n")

        with patch('sys.stdout', new = StringIO()) as output:
            self.otpService.generateOTP(5)
            self.otpService.validateOTP("")
            self.assertEqual(output.getvalue(), "Given OTP was incorrect\n")


if __name__ == '__main__':
    unittest.main()