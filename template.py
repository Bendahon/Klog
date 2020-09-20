# KLog Addon module
# Hardcoded functions here
# __get_ip__ needs to return a list of IP addresses/Hostnames
# __msg_handle__ takes in all parts of the syslog message, returns what to send to the smtp server

class MessageHandle:
    def __init__(self, systype, hostname, servicename, errormessage, date, time, priority=1):
        self.system_type = systype
        self.hostname = hostname
        self.service_name = servicename
        self.error_message = errormessage
        self.date = date
        self.time = time
        self.priority = priority


def __get_ip__():
    """
    :return: a list of IPs, if using hostname must be valid hostname chars (a-Z | 0-9)
    """
    IPList = ["127.0.0.1", "localhost"]
    return IPList


def __msg_handle__(systype, hostname, servicename, errormessage, date, time, priority=1):
    # Make the class. If you don't want to use it, remove it
    x = MessageHandle(systype, hostname, servicename, errormessage, date, time, priority)
    # do what you need to modify and change code here, make sure its efficient
    # CODE HANDLES HERE
    # Return
    return ""
