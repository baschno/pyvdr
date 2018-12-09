#!/usr/bin/env python3

import re
import socket


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

        if isinstance(cmd, unicode):
            cmd = cmd.encode("utf-8")

        self.socket.sendall(cmd)

    def _parse_response(self, resp):
        # <Reply code:3><-|Space><Text><Newline>
        matchobj = re.match(r'^(\d{3})(.)(.*)', resp, re.M | re.I)

        return matchobj.group(1), matchobj.group(2), matchobj.group(3)

    def read_response(self):
        for line in self.socket_file:
            code, separator, value = self._parse_response(line)
            self.responses.append((code, separator, value))

            if separator != '-' and len(self.responses) > 1:
                break

    def get_response_text(self):
        self.read_response()
        print("".join(str(self.responses)))

    def get_response(self):
        self.read_response()
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
