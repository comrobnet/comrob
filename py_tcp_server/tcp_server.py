"""
The TcpServer class sets up the TCP server and handles the communication with the uArm-Python-SDK.
"""
import json
import socket


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

    @staticmethod
    def function_from_json(class_object, function_json):
        """
        Receives an object and a function including args and kwargs and calls the respective function of the object.
        :param class_object: object of which function is called
        :type class_object: any
        :param function_json: json string defining function and args/kwargs.
        :type function_json: str
        """
        function_dict = json.loads(function_json)
        # get corresponding function of object
        function = getattr(class_object, function_dict["function"])
        # set args and kwargs
        args = function_dict["args"]
        kwargs = function_dict["kwargs"]
        function(*args, **kwargs)

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
        self.__tcp_socket.settimeout(timeout)
        self.__tcp_socket.listen(1)
        # wait for connection
        connection, client_address = self.__tcp_socket.accept()
        return connection

    def close(self):
        """
        Close connection.
        """
        self.__tcp_socket.close()
