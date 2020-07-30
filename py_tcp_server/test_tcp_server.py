"""
Test file for  tcp_server.py.
"""
import json
import socket
import threading
import time
import unittest

from py_tcp_server.mock_swift_api import MockSwiftApi
from py_tcp_server.tcp_server import TcpServer


class TestTcpServer(unittest.TestCase):
    """
    Test class for TcpServer class.
    """
    def setUp(self):
        self.tcp_server = TcpServer()
        super().setUp()

    def tearDown(self):
        self.tcp_server.close()
        super().tearDown()

    def test_init(self):
        """
        Test init, connecting and close.
        """
        with self.assertRaises(socket.timeout) as raised:
            self.tcp_server.connect("localhost", 10000, 1)

    # TODO (ALR): This test produces a ResourceWarning, needs to be investigated.
    def test_connect(self):
        """
        Test connecting with tcp server.
        """
        # run server in separate thread
        t_server = threading.Thread(target=self.tcp_server.connect, args=("localhost", 10002, 10), daemon=True)
        t_server.start()
        time.sleep(0.001)
        fake_client = socket.socket()
        fake_client.settimeout(10)
        fake_client.connect(("localhost", 10002))
        fake_client.close()
        t_server.join()

    def test_convert_json_to_function(self):
        """
        Test converting json message to corresponding function.
        """
        # def set_position(self, x=None, y=None, z=None, speed=None, relative=False, wait=False, timeout=10,
        # callback=None, cmd='G0')
        test_dict_1 = {"function": "set_position", "args": [0.0, 0.0, 10.0],
                       "kwargs": {"wait": True, "timeout": 15}}
        test_json_1 = json.dumps(test_dict_1)
        mock_swift = MockSwiftApi()
        self.tcp_server.function_from_json(mock_swift, test_json_1)


if __name__ == '__main__':
    unittest.main()
