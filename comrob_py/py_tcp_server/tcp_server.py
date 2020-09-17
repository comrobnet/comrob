"""
The TcpServer class sets up the TCP server and handles the communication with the uArm-Python-SDK.
"""
import socket

from comrob_py.robot_handler.comrob_error import ComrobError, ErrorCode


#DEPRECTAED - might be useful in future projects
class TcpServer:
    """
    The TcpServer class sets up the TCP server and handles the communication with the uArm-Python-SDK.
    """
    def __init__(self):
        """
        Start server on initialisation
        """
        # create a TCP/IP socket
        self.__tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # allow socket to reuse address
        self.__tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __del__(self):
        """
        Destructor of TcpSever, making sure connection is closed.
        """
        self.close()

    @staticmethod
    def function_from_json(class_object, function_dict):
        """
        Receives an object and a function including args and kwargs and calls the respective function of the object.
        :param class_object: object of which function is called
        :type class_object: any
        :param function_dict: dict from json message.
        :type function_dict: dict
        """
        try:
            # get corresponding function of object
            function = getattr(class_object, function_dict["function"])
            # set args and kwargs
            args = function_dict["args"]
            kwargs = function_dict["kwargs"]
            function(*args, **kwargs)
        except AttributeError:
            raise ComrobError(ErrorCode.E0000, "Attribute function of object not found.")
        except KeyError:
            raise ComrobError(ErrorCode.E0001, "Key Error.")
        except TypeError:
            raise ComrobError(ErrorCode.E0002, "Unexpected keyword argument.")
        except Exception:
            # make sure only comrob errors are raised inside the function
            raise ComrobError(ErrorCode.E0003, "Calling function from Message failed.")

    def connect(self, address, port, timeout):
        """
        Wait for connection on address/port, raise error on timeout.
        :param address: address of tcp server (e.g. 'localhost')
        :type address: string
        :param port: port of tcp server (e.g. 10000)
        :type port: int
        :param timeout: timeout duration in seconds.
        :type timeout: float
        :return: connection to client
        :rtype socket.connection
        """
        try:
            # bind to the address of the port and enable listening
            self.__tcp_socket.bind((address, port))
            self.__tcp_socket.settimeout(timeout)
            self.__tcp_socket.listen(1)
            # wait for connection
            connection, client_address = self.__tcp_socket.accept()
            return connection
        except socket.timeout:
            raise ComrobError(ErrorCode.E0004, "Connection failed - timeout.")
        except OSError as error:
            if error.errno == 98:
                raise ComrobError(ErrorCode.E0005, "Connection failed - address already in use.")
            raise ComrobError(ErrorCode.E0006, "Connection failed - OS error")
        except Exception:
            raise ComrobError(ErrorCode.E0007, "Connection failed.")

    def close(self):
        """
        Close connection.
        """
        self.__tcp_socket.close()
