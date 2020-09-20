# <----------------------------------------->
# | Part of the klog family                 |
# | Client side to talk to the TCP server   |
# | Called from module_handle but if run    |
# | I'll just throw a TEST at the server    |
# | Bendahon 2020                           |
# | Tell you that you're close but no cigar |
# <----------------------------------------->
import zmq
import psutil
import os
from configparser import ConfigParser
from configparser import MissingSectionHeaderError
configurator_file_name = "./conf/configurator.ini"
ConfigBindIP = ""


def check_config():
    global ConfigBindIP
    try:
        try:
            config = ConfigParser()
            config.read(configurator_file_name)
            config_syslog = config["Syslog"]
            ConfigBindIP = config_syslog["Hostname"]
        except KeyError:
            print("Missing Key Error")
    except MissingSectionHeaderError:
        print("Missing the Section header")


def send_message(message_to_send):
    # TODO Add a timeout, maybe learn to do this properly
    if not is_server_running():
        return "Server not running"
    zmq_socket_conn = zmq.Context()
    socket = zmq_socket_conn.socket(zmq.REQ)
    print(f"Bind to {ConfigBindIP}")
    socket.connect(f"tcp://{ConfigBindIP}:45687")
    socket.send(f"{message_to_send}".encode())
    rec_message = socket.recv()
    zmq_socket_conn.destroy()
    socket.close()
    return rec_message.decode('utf-8')


def is_server_running():
    try:
        file = open("./tmp/pid", "r")
        readme = file.read()
        file.close()
    except FileNotFoundError:
        return False

    for i in psutil.process_iter():
        pid = str(i.pid)
        if pid == readme and i.name() == "python":
            return True
    return False


if __name__ == '__main__':
    check_config()
    send_message(b"Can you hear me Rick")
