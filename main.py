"""
This file contains the main fucntion of the Python TCP server / robot controller.
"""

import socket
import time

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
    port = 10017
    connect_timeout = 5
    data_buffer_size = 4096
    # main loop
    while True:
        server = TcpServer()
        print("comrob: Connecting to ", address, ", port: ", port, ".")
        try:
            # this serves as a time.sleep as well
            connection = server.connect(address, port, connect_timeout)
            "comrob: Connected."
            data = connection.recv(data_buffer_size)
            try:
                # call function
                TcpServer.function_from_json(swift, data)
            except Exception:
                # TODO (ALR): replace with message
                print("comrob: failed to call function")


        except socket.timeout:
            server.close()
            print("comrob: failed to connect - timeout")


if __name__ == '__main__':
    main()