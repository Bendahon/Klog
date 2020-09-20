# <--------------------------------------->
# | Needed a place to store all my regexs |
# | Bendahon 2020                         |
# | I've been here before, a few times    |
# <--------------------------------------->
import re


def return_list_of_list(string_of_lists):
    """
    This one i'm pretty proud of. Extract all legal chars from hostnames or IPS
    Used to pass between syslog_server and module_handle
    """
    list_of_lists = []
    # So cool
    regex = r"(\[[0-9a-zA-Z'., ]*\])"
    searchy = re.findall(regex, string_of_lists)
    for i in searchy:
        tmp = i.replace("'", "").strip("][").split(', ')
        list_of_lists.append(tmp)
    return list_of_lists


def get_hostname(syslog_message):
    return re.search(r"[0-9][0-9]:[0-9][0-9]:[0-9][0-9] ([a-z0-9.]*)", syslog_message).group(1)


def get_service_name(syslog_message):
    return re.search(r"([a-z]*)\[[0-9]*]:", syslog_message).group(1).strip()


def get_error_message(syslog_message):
    return re.sub(r"^.*?: ", "", syslog_message)


def get_time(syslog_message):
    return re.search(r"[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", syslog_message).group(0)


def get_date(syslog_message):
    return re.search(r"<[0-9]*>([A-z]* [0-9]*)", syslog_message).group(1)


def get_priority(syslog_message):
    return re.search(r"<([0-9]*)>", syslog_message).group(1)
