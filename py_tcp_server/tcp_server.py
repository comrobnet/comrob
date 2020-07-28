"""
The TcpServer class sets up the TCP server and handles the communication with the uArm-Python-SDK.
"""
import socket
import sys
import time


class TcpServer:
    """
    The TcpServer class sets up the TCP server and handles the communication with the uArm-Python-SDK.
    """
    def __init__(self):
        """
        Start server on initialisation
        """
        # Create a TCP/IP socket
        self.__tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        """
        Destructor of TcpSever, making sure connection is closed.
        """
        self.close()

    def connect(self, address, port, timeout):
        """
        Wait for connection on address/port, raise error on timeout.
        :param address: address of tcp server (e.g. 'localhost')
        :type address: string
        :param port: port of tcp server (e.g. 10000)
        :type port: int
        :param timeout: timeout duration in seconds.
        :type timeout: int
        :return: connection to client
        :rtype socket.connection
        """
        # bind to the address of the port and enable listening
        self.__tcp_socket.bind((address, port))
        self.__tcp_socket.listen(1)
        self.__tcp_socket.settimeout(timeout)
        # wait for connection
        connection, client_address = self.__tcp_socket.accept()
        return connection

    def close(self):
        """
        Close connection.
        """
        self.__tcp_socket.close()
