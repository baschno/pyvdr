#!/usr/bin/env python3

import re
import socket
from collections import namedtuple

response_data = namedtuple('ResponseData', 'Code Separator Value')

class SVDRP(object):
    def __init__(self, hostname = 'localhost', port = 6419):
        self.hostname = hostname
        self.port = port
        self.socket = None
        self.socket_file = None
        self.responses = []

    def connect(self):
        if self.socket is None:
            self.socket = socket.create_connection((self.hostname, self.port), timeout=10)
            self.socket_file = self.socket.makefile('r')

    def send_cmd(self, cmd):
        cmd += '\r\n'

        if isinstance(cmd, str):
            cmd = cmd.encode("utf-8")

        self.socket.sendall(cmd)

    def _parse_response(self, resp):
        # <Reply code:3><-|Space><Text><Newline>
        matchobj = re.match(r'^(\d{3})(.)(.*)', resp, re.M | re.I)

        return response_data(Code=matchobj.group(1), Separator=matchobj.group(2), Value=matchobj.group(3))

    """
    Gets the response from the last CMD and puts it in the internal list.
    :return Namedtuple (Code, Separator, Value)
    """
    def _read_response(self):
        for line in self.socket_file:
            response_entry = self._parse_response(line)
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
        self._read_response()
        print("".join(str(self.responses)))

    """
    Gets the response of the latest CMD as data structure
    :return List of Namedtuple (Code, Separator, Value)
    """
    def get_response(self):
        self._read_response()
        return self.responses

    def shutdown(self):
        self.send_cmd("quit")
        self.socket_file.close()
        self.socket.close()
        self.responses = None


if __name__ == '__main__':
    print("SVDRP")
    svdrp = SVDRP(hostname = 'easyvdr.fritz.box')
    svdrp.connect()
    svdrp.send_cmd("HELP")
    svdrp.get_response_text()
    svdrp.shutdown()
