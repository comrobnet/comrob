"""
This file contains the main function of the Python TCP server / robot controller.
"""
import json
import re
import time

from collections import deque

from comrob_py.robot_handler.comrob_error import ComrobError
from comrob_py.robot_handler.mock_swift_api import MockSwiftApi
from comrob_py.py_tcp_server.tcp_server import TcpServer
from uarm_python_sdk.uarm.wrapper import SwiftAPI


#DEPRECATED
def main():
    # connect to uArm
    try:
        swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
        print("comrob: Connected to robot.")
    except Exception:
        # can not be done differently due to coding of swift API
        swift = MockSwiftApi()
        print("comrob: Connected to mock robot.")

    # server arguments
    address = "localhost"
    port = 10002
    connect_timeout = 60
    data_buffer_size = 4096

    # main loop
    while True:
        time.sleep(0.1)
        print("comrob: Starting TCP server.")
        server = TcpServer()

        # connect to client
        while True:
            print("comrob: Connecting to ", address, ", port: ", port, ".")
            try:
                connection = server.connect(address, port, connect_timeout)
                print("comrob: Connected.")
                break
            except ComrobError as error:
                print("comrob: ", error.message)

        # read messages until connection is closed
        data_queue = deque()
        while True:
            time.sleep(0.1)
            # receive data as bytes
            data = connection.recv(data_buffer_size).decode("utf-8")
            # split multiple messages if needed
            data_list = re.split('(\{.*?\})(?= *\{)', data)
            # add messages to message queue, remove empty messages
            [data_queue.append(element) for element in data_list if len(element) != 0]
            if len(data_queue) != 0:
                message = json.loads(data_queue.popleft())
                if message["disconnect"]:
                    print("comrob: Disconnected.")
                    break
                try:
                    # call function
                    TcpServer.function_from_json(swift, message)
                except ComrobError as error:
                    # TODO (ALR): send TCP message to client for success / failure?
                    print("comrob: ", error.message)

        server.close()


if __name__ == '__main__':
    main()
