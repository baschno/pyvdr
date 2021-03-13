#!/usr/bin/env python3

import re
import socket
import logging
from collections import namedtuple

SVDRP_CMD_QUIT = 'quit'
SVDRP_CMD_LF = '\r\n'
response_data = namedtuple('ResponseData', 'Code Separator Value')
SVDRP_EMPTY_RESPONSE = ""

_LOGGER = logging.getLogger(__name__)


class SVDRP(object):
    SVDRP_STATUS_OK = '250'

    def __init__(self, hostname='localhost', port=6419, timeout=10):
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.responses = []

    def connect(self):
        if self.socket is None:
            try:
                _LOGGER.debug("Setting up connection to {}".format(self.hostname))
                self.socket = socket.create_connection((self.hostname, self.port), timeout=self.timeout)
                self.responses = []
            except socket.error as se:
                _LOGGER.info('Unable to connect. Not powered on? {}'.format(se))

    def is_connected(self):
        return self.socket is not None

    def disconnect(self, send_quit=False):
        _LOGGER.debug("Closing communication with server.")
        if self.socket is not None:
            if send_quit:
                self.socket.sendall(SVDRP_CMD_QUIT.join(SVDRP_CMD_LF).encode())
            self.socket.close()
            self.socket = None

    """
    Sends a SVDRP command to the VDR instance, by default the connection will be created and also be closed at the end.
    If the connection should be kept open in the end (e.g. for sending multi-commands)
    the param auto_disconnect needs to be set to False on invoking.
    The result will be stored in the internal responses array for later content handling.
    :return void / nothing
    """
    def send_cmd(self, cmd, auto_disconnect=True):
        if not self.is_connected():
            return None

        cmds = [cmd]
        cmds.extend([SVDRP_CMD_QUIT] if auto_disconnect else [])
        _LOGGER.debug("Send cmds: {}".format(cmds))

        try:
            data = list()
            [self.socket.sendall(s.join(SVDRP_CMD_LF).encode()) for s in cmds]
            while True:
                data.append(self.socket.recv(32))
                if not data[-1]:
                    break
        except IOError as e:
            _LOGGER.debug("IOError e {}, closing connection".format(e))

        finally:
            _LOGGER.debug('Decoding data into responses: %s' % data)
            response_raw = b''.join(data)
            [self.responses.append(self._parse_response_item(s.decode())) for s in response_raw.splitlines()]
            if auto_disconnect:
                _LOGGER.debug("Auto-closing connection.")
                self.disconnect()
    """
    Parses the response from text into data set
    :return response_data object
    """
    def _parse_response_item(self, resp):
        # <Reply code:3><-|Space><Text><Newline>
        matchobj = re.match(r'^(\d{3})(.)(.*)', resp, re.M | re.I)

        return response_data(Code=matchobj.group(1), Separator=matchobj.group(2), Value=matchobj.group(3))

    """
    Gets the response from the last CMD and puts it in the internal list.
    :return Namedtuple (Code, Separator, Value)
    """
    def _read_response_(self):

        for line in self.responses:
            response_entry = self._parse_response_item(line)
            self.responses.append(response_entry)

            # The first and last row are separated simply by ' ', other with '-'.
            # End once found a ' ' separator
            if response_entry.Separator != '-' and len(self.responses) > 1:
                break

    """
    Gets the response of the latest CMD as plaintext
    :return response as plain text
    """
    def get_response_as_text(self):
        return "".join(str(self.responses))

    """
    Gets the response of the latest CMD as data structure
    By default returns a list, if single line set to true it will just return the
    1st state line.
    :return List of Namedtuple (Code, Separator, Value)
    """
    def get_response(self, single_line=False):
        if not self.is_connected():
            return SVDRP_EMPTY_RESPONSE

        if single_line:
            _LOGGER.debug("Returning single item")
            return self.responses[2]
        else:
            _LOGGER.debug("Returning {} items".format(len(self.responses)))
            return self.responses
