"""
Test file for  tcp_server.py.
"""
import json
import socket
import threading
import time
import unittest

from comrob_py.robot_handler.comrob_error import ComrobError, ErrorCode
from comrob_py.robot_handler.mock_swift_api import MockSwiftApi
from comrob_py.py_tcp_server.tcp_server import TcpServer


class TestTcpServer(unittest.TestCase):
    """
    Test class for TcpServer class.
    """
    def setUp(self):
        self.__tcp_server = TcpServer()
        super().setUp()

    def tearDown(self):
        self.__tcp_server.close()
        super().tearDown()

    def test_init(self):
        """
        Test init, connecting and close.
        """
        with self.assertRaises(ComrobError) as raised:
            self.__tcp_server.connect("localhost", 10000, 1)

    # TODO (ALR): This test produces a ResourceWarning, needs to be investigated.
    def test_connect(self):
        """
        Test connecting with tcp server.
        """
        # test connecting to server in separate thread
        t_server = threading.Thread(target=self.__tcp_server.connect, args=("localhost", 10002, 10), daemon=True)
        t_server.start()
        time.sleep(0.001)
        fake_client = socket.socket()
        fake_client.settimeout(10)
        fake_client.connect(("localhost", 10002))
        fake_client.close()
        t_server.join()

        # test timeout
        timeout_socket = TcpServer()
        with self.assertRaises(ComrobError) as raised:
            timeout_socket.connect("localhost", 10005, 0.01)
        self.assertEqual(raised.exception.error_code, ErrorCode.E0004)

        # test address already in use error
        address_socket_1 = TcpServer()
        address_socket_2 = TcpServer()
        with self.assertRaises(ComrobError) as raised:
            address_socket_1.connect("localhost", 10005, 1)
            address_socket_2.connect("localhost", 10005, 1)
        self.assertEqual(raised.exception.error_code, ErrorCode.E0005)

    def test_convert_json_to_function(self):
        """
        Test converting json message to corresponding function.
        """
        # def set_position(self, x=None, y=None, z=None, speed=None, relative=False, wait=False, timeout=10,
        # callback=None, cmd='G0')
        test_dict_1 = {"function": "set_position", "args": [0.0, 0.0, 10.0],
                       "kwargs": {"wait": True, "timeout": 15},
                       "disconnect": False}
        test_json_1 = json.dumps(test_dict_1)
        test_dict_2 = json.loads(test_json_1)
        mock_swift = MockSwiftApi()
        self.__tcp_server.function_from_json(mock_swift, test_dict_2)

        # test for different errors
        # function name not found
        test_dict_3 = {"function": "no_function", "args": [0.0, 0.0, 10.0],
                       "kwargs": {"wait": True, "timeout": 15},
                       "disconnect": False}
        with self.assertRaises(ComrobError) as raised:
            self.__tcp_server.function_from_json(mock_swift, test_dict_3)
        self.assertEqual(raised.exception.error_code, ErrorCode.E0000)

        # keywords not found
        test_dict_4 = {"function": "set_position",
                       "kwargs": {"wait": True, "timeout": 15},
                       "disconnect": False}
        with self.assertRaises(ComrobError) as raised:
            self.__tcp_server.function_from_json(mock_swift, test_dict_4)
        self.assertEqual(raised.exception.error_code, ErrorCode.E0001)

        # invalid kwargs
        test_dict_5 = {"function": "set_position",
                       "args": [0.0, 0.0, 10.0],
                       "kwargs": {"wait": True, "timeout": 15, "no_keyword": 1},
                       "disconnect": False}
        with self.assertRaises(ComrobError) as raised:
            self.__tcp_server.function_from_json(mock_swift, test_dict_5)
        self.assertEqual(raised.exception.error_code, ErrorCode.E0002)


if __name__ == '__main__':
    unittest.main()
