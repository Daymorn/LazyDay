
import os
import sys
import struct
import socket
import threading
import types
import time

from .config import HOST, MSG_TIMEOUT, SOCK_TIMEOUT
from ._datatypes import *
from . import winapi

__author__ = 'ZeroDX'
__version__ = 1.4


EVENTS_NAMES = (
    'eviteminfo', 'evitemdeleted', 'evspeech', 'evdrawgameplayer',
    'evmoverejection', 'evdrawcontainer', 'evadditemtocontainer',
    'evaddmultipleitemsincont', 'evrejectmoveitem', 'evupdatechar',
    'evdrawobject', 'evmenu', 'evmapmessage', 'evallowrefuseattack',
    'evclilocspeech', 'evclilocspeechaffix', 'evunicodespeech',
    'evbuffdebuffsystem', 'evclientsendresync', 'evcharanimation',
    'evicqdisconnect', 'evicqconnect', 'evicqincomingtext', 'evicqerror',
    'evincominggump', 'evtimer1', 'evtimer2', 'evwindowsmessage', 'evsound',
    'evdeath', 'evquestarrow', 'evpartyinvite', 'evmappin', 'evgumptextentry',
    'evgraphicaleffect', 'evircincomingtext', 'evmessengerevent',
    'evsetglobalvar', 'evupdateobjstats', 'evglobalchat'
)

EVENTS_ARGTYPES = _str, _uint, _int, _ushort, _short, _ubyte, _byte, _bool


class Connection:
    port = None

    def __init__(self):
        self._sock = socket.socket()

        self._buffer = bytes()
        self.pause = False
        self.results = {}
        self.callbacks = {}
        for i in range(len(EVENTS_NAMES)):
            self.callbacks[i] = None

    def connect(self, host=None, port=None):
        if host is None:
            host = HOST
        if port is None:
            if self.port is None:
                port = get_port()
                self.__class__.port = port
            else:
                port = self.port
        self._sock.settimeout(SOCK_TIMEOUT)
        self._sock.connect((host, port))
        self._sock.setblocking(False)

    def close(self):
        self._sock.close()

    def receive(self, size=4096):
        # try to get a new data from socket
        data = b''
        try:
            data += self._sock.recv(size)
            if not data:
                err = 'Connection to Stealth was lost.'
                winapi.MessageBox(0, err.decode() if b'' == '' else err,
                                  'Error'.decode() if b'' == '' else 'Error', 0)
                exit(1)
        except socket.error:
            return
        # parse data
        offset = 0
        while 1:
            if self._buffer:  # if some data was already stored
                data = self._buffer + data
                self._buffer = bytes()
            # parse packet header
            if len(data) < 10:
                self._buffer += data
                break
            size, type_, length = struct.unpack_from('=IHI', data, offset)
            if size > len(data):
                self._buffer += data
                break
            offset += 10
            # packet type is 1 (a returned value)
            if type_ == 1:
                index = struct.unpack_from('H', data, offset)[0]
                self.results[index] = data[offset+2:offset+length]
                offset += length
            # packet type is 3 (an event callback)
            elif type_ == 3:
                index, count = struct.unpack_from('=2B', data, offset)
                offset += 2
                # parse args
                args = []
                for i in range(count):
                    argtype = EVENTS_ARGTYPES[struct.unpack_from('B', data,
                                                                 offset)[0]]
                    offset += 1
                    arg = argtype.from_buffer(data, offset)
                    offset += struct.calcsize(arg.fmt)
                    args.append(arg.value)
                # run handler
                self.callbacks[index](*args)
            # packet type is 4 (a pause script packet)
            elif type_ == 4:
                self.pause = True if not self.pause else False
                offset += length
            # packet type is 2 (terminate script)
            elif type_ == 2:
                exit(0)
            if offset >= len(data):
                break

    def send(self, data):
        self._sock.send(data)


class ScriptMethod:
    argtypes = []
    restype = None

    def __init__(self, index):
        self.index = index

    def __call__(self, *args):
        conn = get_connection()
        conn.receive()  # check pause or events
        while conn.pause:
            conn.receive()
            time.sleep(.01)
        if not self.index:  # wait
            return
        # pack args
        data = bytes()
        for cls, val in zip(self.argtypes, args):
            data += cls(val).serialize()
        # form packet
        header = struct.pack('=HI', self.index, len(data))
        size = struct.pack('!I', len(header+data))
        # send to the stealth
        conn.send(size+header+data)
        # wait for a result if required
        while self.restype is not None:
            conn.receive()
            try:
                result = self.restype.from_buffer(conn.results.pop(self.index))
                return result.value
            except KeyError:
                time.sleep(.001)


def get_port():
    # First way - get port from cmd parameters.
    # If script was launched as internal script from Stealth.
    if len(sys.argv) >= 3 and sys.argv[2].isalnum():
        return int(sys.argv[2])
    # Second way - ask Stealth for a port number via windows messages.
    # If script was launched as external script.
    wnd = 'TStealthForm'.decode() if b'' == '' else 'TStealthForm'  # py2
    hwnd = winapi.FindWindow(wnd, None)
    if not hwnd:
        error = 'Can not find Stealth window.'
        winapi.MessageBox(0, error.decode() if b'' == '' else error,  # py2
                           'Error'.decode() if b'' == '' else 'Error', 0)
        exit(1)
    # form copydata
    pid = '{pid:08X}'.format(pid=os.getpid())
    lp = (pid + os.path.basename(sys.argv[0])).encode() + b'\x00'
    cb = len(lp)
    dw = winapi.GetCurrentThreadId()
    copydata = winapi.COPYDATA(dw, cb, lp)
    # send message
    winapi.SetLastError(0)
    if not winapi.SendMessage(hwnd, winapi.WM_COPYDATA, 0, copydata.pointer):
        error = 'Can not send message. ErrNo: {}'.format(winapi.GetLastError())
        winapi.MessageBox(0, error.decode() if b'' == '' else error,  # py2
                           'Error'.decode() if b'' == '' else 'Error', 0)
        exit(1)
    # wait for an answer
    msg = winapi.MSG()
    now = time.time()
    while now + MSG_TIMEOUT > time.time():
        if winapi.PeekMessage(msg, 0, winapi.FM_GETFOCUS,
                              winapi.FM_GETFOCUS, winapi.PM_REMOVE):
            while len(sys.argv) < 3:
                sys.argv.append('')
            sys.argv[2] = str(msg.wParam)
            return msg.wParam
        else:
            time.sleep(0.005)
    error = 'PeekMessage timeout'
    winapi.MessageBox(0, error.decode() if b'' == '' else error,  # py2
                       'Error'.decode() if b'' == '' else 'Error', 0)  # py2
    exit(1)


def get_connection():
    def join(self, timeout=None):
        self.connection.close()
        self.__class__.join(self, timeout)

    thread = threading.current_thread()
    if hasattr(thread, 'connection'):
        return thread.connection
    thread.connection = Connection()
    thread.connection.connect()
    thread.join = types.MethodType(join, thread)  # close socket for each one
    return thread.connection
