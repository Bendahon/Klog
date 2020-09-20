# <---------------------------------------------------->
# | Klog                                               |
# | Combo of Klog, KDE and syslog                      |
# | Main process, everything else is called separately |
# | Bendahon 2020                                      |
# | His names Tom Sawyer                               |
# <---------------------------------------------------->

import socketserver
import subprocess
import syslog_regexs
from configparser import ConfigParser
from configparser import MissingSectionHeaderError
import glob
import importlib

ConfigGlobalLog = 'global.log'
__version__ = 0.4
configurator_file_name = "./conf/configurator.ini"
ConfigHostname = ""
ConfigPort = 0
ConfigIndLog = ""
Addons = []


def check_config():
    global ConfigHostname
    global ConfigPort
    global ConfigGlobalLog
    global ConfigIndLog
    try:
        try:
            config = ConfigParser()
            config.read(configurator_file_name)
            config_syslog = config["Syslog"]
            ConfigHostname = config_syslog["Hostname"]
            ConfigPort = config_syslog["Port"]
            config_logging = config["Logging"]
            ConfigGlobalLog = config_logging["Global_log"]
            ConfigIndLog = config_logging["Individual_base"]
            try:
                ConfigPort = int(ConfigPort)
            except ValueError:
                print("Port isn't an int")
                exit(1)
        except KeyError:
            print("Missing Key Error")
    except MissingSectionHeaderError:
        print("Missing the Section header")


def get_addons():
    global Addons
    for i in glob.glob("./addons/*.py"):
        opls = []
        mymodule = importlib.import_module(i.replace(".py", "").replace("./", "").replace("/", "."))
        opls.append(mymodule.__name__)
        opls.append(mymodule.__get_ip__())
        Addons.append(opls)


class SyslogUDPHandle(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        # TODO get rid of this printing
        print(data)
        handle_rec_msg(data)


def handle_rec_msg(syslog_message):
    ip_or_hostname = syslog_regexs.get_hostname(syslog_message)
    # write to a ip/hostname file and then a global
    write_to_file(syslog_message, f"{ConfigIndLog}{ip_or_hostname}")
    write_to_file(syslog_message, ConfigGlobalLog)
    subprocess.Popen([f"python3 ./module_handle.py '{syslog_message}' {Addons}"],
                     shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)


def write_to_file(message, hostname_or_filename=ConfigGlobalLog):
    file = open(hostname_or_filename, "a+")
    file.write(f"{message}\n")
    file.close()


if __name__ == '__main__':
    write_to_file("Starting syslog_server")
    write_to_file(f"Version: {__version__}")
    write_to_file("Checking Config file")
    check_config()
    write_to_file("Getting the addon files")
    get_addons()
    # Start the UDP server
    try:
        server = socketserver.UDPServer((ConfigHostname, ConfigPort), SyslogUDPHandle)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")
