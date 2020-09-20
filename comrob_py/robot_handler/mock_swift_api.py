"""
This file provides the MockSwiftApi class.
"""


class MockSwiftApi:
    """
    This class mocks the Swift Api class, printing all function calls.
    """
    def __init__(self, port=None, baudrate=115200, timeout=None, **kwargs):
        print("__init__ ", port, baudrate, timeout)

    def connect(self, port=None, baudrate=None, timeout=None):
        print("connect ", port, baudrate, timeout)

    def disconnect(self, is_clean=True):
        print("disconnect ", is_clean)

    def waiting_ready(self, timeout=5, **kwargs):
        print("waiting_ready ", timeout)

    def reset(self, speed=None, wait=True, timeout=None, x=200, y=0, z=150):
        print("resest ", speed, wait, timeout, x, y, z)

    def set_mode(self, mode=0, wait=True, timeout=None, callback=None):
        print("set_mode ", mode, wait, timeout, callback)

    def get_position(self, wait=True, timeout=None, callback=None):
        print("get_position ", wait, timeout, callback)
        return [0, 0, 0]

    def set_position(self, x=None, y=None, z=None, speed=None, relative=False, wait=False, timeout=10, callback=None, cmd='G0'):
        print("set_position ", x, y, z, speed, relative, wait, timeout, callback, cmd)

    def set_servo_angle(self, servo_id=0, angle=90, wait=False, timeout=10, speed=None, callback=None):
        print("set_servo_angle ", servo_id, angle, wait, timeout, speed, callback)

    def set_wrist(self, angle=90, wait=False, timeout=10, speed=None, callback=None):
        print("set_wrist ", angle, wait, timeout, speed, callback)

    def set_pump(self, on=False, timeout=None, wait=True, check=False, callback=None):
        print("set_pump ", on, timeout, wait, check, callback)

    def flush_cmd(self, timeout=None, wait_stop=False):
        print("flush_cmd ", timeout, wait_stop)

