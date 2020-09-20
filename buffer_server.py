# <--------------------------------------------->
# | Part of the klog family                     |
# | Just run endlessly                          |
# | Recieve the message, buffer and forward     |
# | Bendahon 2020                               |
# | I know I'm running circles but I can't quit |
# <--------------------------------------------->

# pip install pyzmq
import time
import zmq
import datetime
from datetime import datetime, timedelta
import os
from configparser import ConfigParser
from configparser import MissingSectionHeaderError

buffer = []
trigger_time = datetime.now()
configurator_file_name = "./conf/configurator.ini"
ConfigBindIP = ""
ConfigBufferTimeMins = ""


def check_config():
    global ConfigBindIP
    global ConfigBufferTimeMins
    try:
        try:
            config = ConfigParser()
            config.read(configurator_file_name)
            config_syslog = config["Syslog"]
            ConfigBindIP = config_syslog["Hostname"]
            config_buffer = config["BuffServer"]
            ConfigBufferTimeMins = config_buffer["Buffer_time"]
        except KeyError:
            print("Missing Key Error")
    except MissingSectionHeaderError:
        print("Missing the Section header")


def write_pid():
    process_id = os.getpid()
    file = open("./tmp/pid", "w")
    file.write(str(process_id))
    file.close()


def time_to_smtp():
    global trigger_time
    global buffer
    datetime_now = datetime.now()
    if datetime_now > trigger_time:
        print("TRIGGERED")
        trigger_time = datetime.now() + timedelta(minutes=int(ConfigBufferTimeMins))
        print(f"Set to trigger @ {trigger_time}")
        print(f"Now:           @ {datetime_now}")
        buffer = []


def start_server():
    global trigger_time
    print("Server started")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://{ConfigBindIP}:45687")

    trigger_time = trigger_time + timedelta(minutes=int(ConfigBufferTimeMins))
    print(f"Set to trigger Next @ {trigger_time}")
    while True:
        # TODO make sure we can find a way to clear the buffer after X minutes
        message = socket.recv()
        # add message to buffer
        buffer.append(message)
        socket.send(b"Loud and clear Morty")
        time_to_smtp()


if __name__ == '__main__':
    check_config()
    write_pid()
    start_server()
