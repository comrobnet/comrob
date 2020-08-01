"""
This file provides a small test socket to test the main file.
"""

import socket
import json

if __name__ == '__main__':
    address = "localhost"
    port = 10002
    client = socket.socket()
    client.settimeout(10)
    client.connect(("localhost", port))

    # test_dict_1 = {"function": "set_position", "args": [0.0, 0.0, 10.0],
    #                "kwargs": {"wait": True, "timeout": 15}}
    # test_json_1 = json.dumps(test_dict_1)
    #
    # client.send(test_json_1.encode("utf-8"))

    client.close()
