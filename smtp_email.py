# <---------------------------------------------------->
# | SMTP quick and dirty sender                        |
# | Pass in the subject and message and boom boom      |
# | Bendahon 2020                                      |
# | Once more i'll say goodbye to you                  |
# <---------------------------------------------------->
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys
from configparser import ConfigParser
from configparser import MissingSectionHeaderError
configurator_file_name = "./conf/configurator.ini"

ConfigUser = ""
ConfigPass = ""
ConfigHostname = ""
ConfigSendFrom = ""
ConfigSendTo = ""
ConfigReplyTo = ""

# TODO add these in, tls in configurator
# smtp_relay.starttls()
# smtp_relay.ehlo


def check_config():
    global ConfigUser
    global ConfigPass
    global ConfigHostname
    global ConfigSendFrom
    global ConfigSendTo
    global ConfigReplyTo
    try:
        try:
            config = ConfigParser()
            config.read(configurator_file_name)
            config_email = config["Email"]
            ConfigUser = config_email["User"]
            ConfigPass = config_email["Pass"]
            ConfigHostname = config_email["Hostname"]
            ConfigSendFrom = config_email["Send_from"]
            ConfigSendTo = config_email["Send_to"]
            ConfigReplyTo = config_email["Reply_to"]
        except KeyError:
            print("Missing Key Error")
    except MissingSectionHeaderError:
        print("Missing the Section header")


def check_args():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} Subject Message")
        exit(1)


def send_email():
    # construct the message
    email_message = MIMEMultipart()
    email_message['From'] = ConfigSendFrom
    email_message['To'] = ConfigSendTo
    email_message['Subject'] = sys.argv[1]
    email_message['Reply-To'] = ConfigReplyTo
    message = sys.argv[2]
    email_message.attach(MIMEText(message, 'plain'))

    # Connect & Send
    smtp_relay = smtplib.SMTP(ConfigHostname)
    smtp_relay.login(ConfigUser, ConfigPass)
    smtp_relay.sendmail(email_message['From'], email_message['To'], email_message.as_string())
    smtp_relay.quit()
    # print(f"Successfully sent email message to: {(msg['To'])}")


if __name__ == '__main__':
    check_config()
    check_args()
    send_email()
