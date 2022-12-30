
from dotenv import load_dotenv, find_dotenv
from os import environ as env
import random
from re import fullmatch
import smtplib
load_dotenv(find_dotenv())


# Create a file named ".env" in the sample floder where this file is stored and save the keys as below
# EMAIL=your_email
# PASSWORD=email_password (app password)

SENDER_EMAIL = env.get('EMAIL')
SENDER_EMAIL_PASSWD = env.get('PASSWORD')
OTP_LENGTH = int(env.get('OTP_LENGTH'))

# regular expression for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def initMailServer(email, password):
    """
    The function to initialize SMTP server for specific sender id.

    Parameters:
        email (str): The email id of the sender.
        password (str): The password for the email id.

    Returns:
        s (object): SMTP server object.
    """

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(email, password)
    except Exception as e:
        print("\nError occured while initializing mail server")
        print(e)
    else:
        print("\nSMTP server is initialized and running....\n")
        return s


def sendMail(server, msg, receiver):
    """
    The function to send an e-mail to a specific email address.

    Parameters:
        server (object): SMTP server object containing sender information.
        msg (str): The content or body of the email to be sent.
        receiver (str): Email address of the recipient.
    """
    server.sendmail(SENDER_EMAIL, receiver, msg)
    print("\n\tOTP Sent to your mail!\n")


def generateOTP(length):
    """
    The function to generates a random OTP number.

    Parameters:
        length (int): The length of an OTP to be generated.

    Returns:
        otp (str): A random OTP of given length.
    """

    digits = "0123456789"
    otp = random.sample(digits, length)

    return "".join(otp)


def validateEmail(email):
    """
    The function to check if the email is valid

    Parameters:
        email (str): Given valid input email address.
    """

    return fullmatch(regex, email) != None


def getEmail():
    """
    The function to input valid email address.

    Returns:
        email (str): Given valid input email address.
    """

    print("Please Enter your Email to receive OTP")
    email = input("Email: ")

    # While Email is not valid take new input
    while not validateEmail(email):
        print("Please enter a valid email address")
        email = input("Email: ")

    return email


def validateOTP(org_otp):
    """
    The function to validate the OTP sent to the user.

    Parameters:
        org_otp (str): The original OTP generated by the program and sent to user.
    """

    print("Please enter the OTP to proceed")
    otp = input("OTP: ")

    if otp.strip() == org_otp:
        print("Given OTP was correct")
    else:
        print("Given OTP was incorrect")


def main():
    mailServer = initMailServer(SENDER_EMAIL, SENDER_EMAIL_PASSWD)

    if mailServer != None:
        receiver = getEmail()
        OTP = generateOTP(OTP_LENGTH)

        msg = '\n\nThe One Time Password(OTP) is: ' + str(OTP)

        sendMail(mailServer, msg, receiver)
        validateOTP(OTP)

        mailServer.quit()


if __name__ == "__main__":
    main()
