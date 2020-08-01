"""
This file contains the main fucntion of the Python TCP server / robot controller.
"""
import json
import re
import socket
import time

from collections import deque

from py_tcp_server.mock_swift_api import MockSwiftApi
from py_tcp_server.tcp_server import TcpServer
from uarm_python_sdk.uarm.wrapper import SwiftAPI


def main():
    # connect to uArm
    try:
        swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
        print("comrob: Connected to robot.")
    except Exception:
        # can not be done differently due to coding of swift API
        swift = MockSwiftApi()
        print("comrob: Connected to mock robot.")

    # start TCP server
    print("comrob: Starting TCP server.")
    address = "localhost"
    port = 10002
    connect_timeout = 60
    data_buffer_size = 4096
    # main loop
    while True:
        time.sleep(0.1)
        server = TcpServer()
        print("comrob: Connecting to ", address, ", port: ", port, ".")
        try:
            connection = server.connect(address, port, connect_timeout)
            print("comrob: Connected.")
            data_queue = deque()
            # read messages until connection is closed
            while True:
                time.sleep(0.1)
                # receive data as bytes
                data = connection.recv(data_buffer_size).decode("utf-8")
                # split multiple messages if needed
                data_list = re.split('(\{.*?\})(?= *\{)', data)
                [data_queue.append(element) for element in data_list if len(element) != 0]
                if len(data_queue) != 0:
                    message = json.loads(data_queue.popleft())
                    if message["disconnect"]:
                        print("comrob: Disconnected.")
                        break
                    try:
                        # call function
                        TcpServer.function_from_json(swift, message)
                    except Exception:
                        # TODO (ALR): replace with message
                        print("comrob: failed to call function")

        except socket.timeout:
            print("comrob: failed to connect - timeout")
        except OSError as error:
            if error.errno == 98:
                print("comrob: failed to connect - adress already in use.")

        server.close()


if __name__ == '__main__':
    main()
