#!/usr/bin/env python3

import re
from collections import namedtuple
from svdrp import SVDRP

EPG_DATA_RECORD = '215'
epg_info = namedtuple('EPGDATA', 'Channel Title Description')

class PYVDR(object):

    def __init__(self, hostname = 'localhost'):
        self.hostname = hostname
        self.svdrp = SVDRP(hostname = self.hostname)

    def stat(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("STAT DISK")
        return self.svdrp.get_response()[1:]

    def list_recordings(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("LSTC")
        return self.svdrp.get_response()[1:]

    def get_channel(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("CHAN")
        current_channel = self.svdrp.get_response()[-1]
        return current_channel[2]

    def _parse_channel_response(self, channel_data):
        print(channel_data[2])
        channel_info = re.match(r'^(\d*)\s(.*)$', channel_data[2], re.M | re.I)
        return channel_info.group(1), channel_info.group(2)

    def get_channel_info(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("CHAN")
        chan = self.svdrp.get_response()[-1]
        print("##" + str(chan))
        channel_no, channel_name = self._parse_channel_response(chan)

        self.svdrp.send_cmd("LSTE {} now".format(channel_no))
        epg_data = self.svdrp.get_response()[1:]
        print(epg_data)
        for d in epg_data:
            if d[0] == EPG_DATA_RECORD:
                print(d[2])
                epg = re.match(r'^(\S)\s(.*)$', d[2], re.M | re.I)
                if epg is not None:
                    epg_field_type = epg.group(1)
                    epg_field_value = epg.group(2)

                    print(epg_field_type)
                    if epg_field_type == 'T':
                        epg_title = epg_field_value
                    if epg_field_type == 'C':
                        epg_channel = epg_field_value
                    if epg_field_type == 'S':
                        epg_description = epg_field_value

        epg = epg_info(Channel=epg_channel, Title=epg_title, Description=epg_description)



        return channel_no, channel_name, str(epg)

    def channel_up(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("CHAN +")
        return self.svdrp.get_response_text()

    def channel_down(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("CHAN -")
        return self.svdrp.get_response_text()

    def test(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("LSTE 6 now")
        return self.svdrp.get_response_text()

    def finish(self):
        self.svdrp.shutdown()


if __name__ == '__main__':
    print("pyvdr")
    pyvdr = PYVDR(hostname='easyvdr.fritz.box')
    print(pyvdr.get_channel_info())
    pyvdr.finish()
