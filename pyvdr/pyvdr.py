#!/usr/bin/env python3

from svdrp import SVDRP

class PYVDR(object):
    def __init__(self, hostname = 'localhost'):
        self.hostname = hostname
        self.svdrp = SVDRP(hostname = self.hostname)

    def stat(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("STAT DISK")
        return self.svdrp.get_response_text()

    def finish(self):
        self.svdrp.shutdown()


if __name__ == '__main__':
    print("pyvdr")
    pyvdr = PYVDR(hostname='easyvdr.fritz.box')
    print(pyvdr.stat())
    pyvdr.finish()
