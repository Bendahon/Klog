# <---------------------------------------------------------->
# | Invisimodule for KLog                                    |
# | This shouldn't be run on its own unless you're debugging |
# | Bendahon 2020                                            |
# | Hello there, The angel from my nightmare                 |
# <---------------------------------------------------------->

import sys
import syslog_regexs
import importlib
from configparser import ConfigParser
from configparser import MissingSectionHeaderError
import tcp_client

configurator_file_name = "./conf/configurator.ini"
ConfigModuleLog = ""
# Syslog message layout
syslog_priority = ""
syslog_date = ""
syslog_time = ""
syslog_hostname = ""
syslog_service_name = ""
syslog_error_message = ""
_Addons_ = []


def check_config():
    global ConfigModuleLog
    try:
        try:
            config = ConfigParser()
            config.read(configurator_file_name)
            config_syslog = config["Logging"]
            ConfigModuleLog = config_syslog["Module_log"]
        except KeyError:
            print("Missing Key Error")
    except MissingSectionHeaderError:
        print("Missing the Section header")


def main():
    # Read the args
    syslog_message = sys.argv[1]
    # Lets set the scene
    set_me_up(syslog_message)
    module_handle()
    gtfo(0)


def set_me_up(syslog_message):
    write_to_log("Setting up")
    global syslog_priority
    global syslog_date
    global syslog_time
    global syslog_hostname
    global syslog_service_name
    global syslog_error_message
    syslog_priority = syslog_regexs.get_priority(syslog_message)
    syslog_date = syslog_regexs.get_date(syslog_message)
    syslog_time = syslog_regexs.get_time(syslog_message)
    syslog_hostname = syslog_regexs.get_hostname(syslog_message)
    syslog_service_name = syslog_regexs.get_service_name(syslog_message)
    syslog_error_message = syslog_regexs.get_error_message(syslog_message)


def module_handle():
    addon_name = ""
    write_to_log("Searching for Addon name")
    for i in _Addons_:
        if syslog_hostname in i:
            addon_name = i[0]
            break

    if addon_name == "":
        write_to_log("Exiting program, Dumping info", "DEBUG")
        write_to_log(f"Addon Name: {addon_name}", "DEBUG")
        write_to_log(f"Hostname: {syslog_hostname}", "DEBUG")
        write_to_log(f"Service Name: {syslog_service_name}", "DEBUG")
        write_to_log(f"Error Message: {syslog_error_message}", "DEBUG")
        write_to_log(f"Date: {syslog_date}", "DEBUG")
        write_to_log(f"Time: {syslog_time}", "DEBUG")
        write_to_log(f"Priority: {syslog_priority}", "DEBUG")
        gtfo(1)

    message_handle = importlib.import_module(addon_name)
    actual_smtp_message = message_handle.__msg_handle__(addon_name, syslog_hostname, syslog_service_name,
                                                        syslog_error_message, syslog_date, syslog_time, syslog_priority)
    write_to_log(f"Final message to SMTP server: {actual_smtp_message}")

    if actual_smtp_message != "":
        write_to_log("Spawning new TCP socket")
        x = tcp_client.send_message(actual_smtp_message)
        write_to_log(f"Server response: {x}")
        write_to_log("Done!")
        gtfo(0)
    gtfo(1)


def write_to_log(stringin, logtype="LOGGING"):
    print(f"{logtype}: {stringin}")
    log_file_module_handle.write(f"{logtype}: {stringin}\n")


def gtfo(exit_code=0):
    write_to_log("Program exiting", "GTFO")
    log_file_module_handle.close()
    exit(exit_code)


if __name__ == '__main__':
    check_config()
    log_file_module_handle = open(ConfigModuleLog, "a+")
    write_to_log("Spawned new instance", "SPAWN")
    _Addons_ = syslog_regexs.return_list_of_list(sys.argv[2])
    write_to_log(f"Addons = {_Addons_}")
    # Let the magic begin
    main()
    gtfo(0)
