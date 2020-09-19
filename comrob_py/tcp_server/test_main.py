"""
This file provides a small test socket to test the main file.
"""

import json
import socket
import time


# DEPRECATED
if __name__ == '__main__':
    address = "localhost"
    port = 10002
    client = socket.socket()
    client.settimeout(10)
    # connect
    client.connect(("localhost", port))
    # 1. message
    test_dict_1 = {"function": "set_position", "args": [0.0, 0.0, 10.0],
                   "kwargs": {"wait": True, "timeout": 15},
                   "disconnect": False}
    test_json_1 = json.dumps(test_dict_1)
    client.send(test_json_1.encode("utf-8"))
    # 2. message disconnect
    time.sleep(3)
    test_dict_2 = {"disconnect": True}
    test_json_2 = json.dumps(test_dict_2)
    client.send(test_json_2.encode("utf-8"))

    client.close()
