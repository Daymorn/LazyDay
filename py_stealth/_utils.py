
import datetime
import errno
import socket
import threading


__author__ = 'ZeroDX'
__version__ = 1.1

__all__ = ['get_main_thread',
           'iterable',
           'ddt2pdt',
           'pdt2ddt',
           'is_socket_alive']


def get_main_thread():  # py2
    try:
        return threading.main_thread()
    except AttributeError:
        for thread in threading.enumerate():
            if isinstance(thread, threading._MainThread):
                return thread


def ddt2pdt(ddt):  # delphi time into py datetime
    start = datetime.datetime(1899, 12, 30)
    hours = abs(ddt - int(ddt)) * 24
    return start + datetime.timedelta(days=int(ddt), hours=hours)


def pdt2ddt(pydt):  # py datetime into delphi time
    start = datetime.datetime(1899, 12, 30)
    delta = pydt - start
    seconds = (delta - datetime.timedelta(days=delta.days)).total_seconds()
    return delta.days + seconds / 3600 / 24


def iterable(obj):
    try:
        for i in obj:
            return True
    except TypeError:
        return False


def is_socket_alive(sock):
    if not sock:
        return False
    try:
        sock.getsockname()
        sock.getpeername()
    except socket.error as exc:
        error = exc.args[0]
        if error == errno.EBADF or error == errno.ENOTCONN:
            return False
        raise
    return True
