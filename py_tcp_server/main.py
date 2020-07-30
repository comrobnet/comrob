"""
This file contains the main fucntion of the Python TCP server / robot controller.
"""

import socket
import time

from py_tcp_server.tcp_server import TcpServer
from uArm-Python-SDK.uarm.wrapper import SwiftAPI

def main():
    # connect to uArm
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

        except socket.timeout:
            server.close()
            print("comrob: failed to connect - timeout")


if __name__ == '__main__':
    main()
