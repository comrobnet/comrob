"""
Test file for  tcp_server.py.
"""
import socket
import threading
import time
import unittest

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
        t_server = threading.Thread(target=self.tcp_server.connect, args=("localhost", 10002, 10), daemon=True)
        t_server.start()
        time.sleep(0.001)
        fake_client = socket.socket()
        fake_client.settimeout(10)
        fake_client.connect(("localhost", 10002))
        fake_client.close()
        t_server.join()


if __name__ == '__main__':
    unittest.main()
