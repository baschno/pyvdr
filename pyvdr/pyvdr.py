#!/usr/bin/env python3

from .svdrp import SVDRP
import re
from collections import namedtuple

EPG_DATA_RECORD = '215'
epg_info = namedtuple('EPGDATA', 'Channel Title Description')
#timer_info = namedtuple('TIMER', 'Status Name Date Description')
#channel_info = namedtuple('CHANNEL', 'Number Name')

FLAG_TIMER_ACTIVE = 1
FLAG_TIMER_INSTANT_RECORDING = 2
FLAG_TIMER_VPS = 4
FLAG_TIMER_RECORDING = 8


class PYVDR(object):

    def __init__(self, hostname='localhost', timeout=10):
        self.hostname = hostname
        self.svdrp = SVDRP(hostname=self.hostname, timeout=timeout)
        self.timers = None

    def sensors(self):
        return ['Vdrinfo']

    def stat(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("STAT DISK")
        disk_stat_response = self.svdrp.get_response()[1:][0]

        if disk_stat_response.Code != SVDRP.SVDRP_STATUS_OK:
            return -1

        disk_stat_parts = re.match(
            r'(\d*)\w. (\d*)\w. (\d*)',
            disk_stat_response.Value, re.M | re.I)
        self.svdrp.disconnect()
        if disk_stat_parts:
            return [disk_stat_parts.group(1),
                    disk_stat_parts.group(2),
                    disk_stat_parts.group(3)]
        else:
            return None

    def get_channel(self):
        self.svdrp.connect()
        if not self.svdrp.is_connected():
            return None

        self.svdrp.send_cmd("CHAN")
        generic_response = self.svdrp.get_response()[-1]
        channel = self._parse_channel_response(generic_response)
        self.svdrp.disconnect()
        return channel

    @staticmethod
    def _parse_channel_response(channel_data):
        channel_info = {}

        channel_parts = re.match(
            r'^(\d*)\s(.*)$',
            channel_data[2],
            re.M | re.I)
        if channel_parts:
            channel_info['number'] = channel_parts.group(1)
            channel_info['name'] = channel_parts.group(2)
        return channel_info

    @staticmethod
    def _parse_timer_response(response):
        timer = {}
        m = re.match(
            r'^(\d) (\d{1,2}):(\d):(\d{4}-\d{2}-\d{2}):(\d{4}):(\d{4}):(\d+):(\d+):(.*):(.*)$',
            response.Value,
            re.M | re.I)

        if m:
            timer['status'] = m.group(2)
            timer['channel'] = m.group(3)
            timer['date'] = m.group(4)
            timer['name'] = m.group(9)
            timer['description'] = ""
            timer['series'] = timer['name'].find('~') != -1
            timer['instant'] = False

        return timer

    def get_timers(self):
        timers = []
        self.svdrp.connect()
        self.svdrp.send_cmd("LSTT")
        responses = self.svdrp.get_response()
        self.svdrp.disconnect()
        for response in responses:
            if response.Code != '250':
                continue
            timers.append(self._parse_timer_response(response))
        return timers

    def is_recording(self):
        self.svdrp.connect()
        if not self.svdrp.is_connected():
            return None

        self.svdrp.send_cmd("LSTT")
        responses = self.svdrp.get_response()
        for response in responses:
            if response.Code != '250':
                continue
            timer = self._parse_timer_response(response)
            self.svdrp.disconnect()
            if self._check_timer_recording_flag(timer, FLAG_TIMER_INSTANT_RECORDING):
                timer['instant'] = True
                return timer
            if self._check_timer_recording_flag(timer, FLAG_TIMER_RECORDING):
                return timer

        return None

    def get_channel_epg_info(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("CHAN")
        chan = self.svdrp.get_response()[-1]
        channel = self._parse_channel_response(chan)
        self.svdrp.send_cmd("LSTE {} now".format(channel['number']))
        epg_data = self.svdrp.get_response()[1:]
        self.svdrp.disconnect()
        for d in epg_data:
            if d[0] == EPG_DATA_RECORD:
                epg = re.match(r'^(\S)\s(.*)$', d[2], re.M | re.I)
                if epg is not None:
                    epg_field_type = epg.group(1)
                    epg_field_value = epg.group(2)

                    if epg_field_type == 'T':
                        epg_title = epg_field_value
                    if epg_field_type == 'C':
                        epg_channel = epg_field_value
                    if epg_field_type == 'D':
                        epg_description = epg_field_value

        return channel, \
               epg_info(Channel=epg_channel,
                        Title=epg_title,
                        Description=epg_description)

    def channel_up(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("CHAN +")
        reponse_text = self.svdrp.get_response_as_text()
        self.svdrp.disconnect()
        return reponse_text

    def channel_down(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("CHAN -")
        reponse_text = self.svdrp.get_response_as_text()
        self.svdrp.disconnect()
        return reponse_text

    def list_recordings(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("LSTR")
        return self.svdrp.get_response()[1:]

    @staticmethod
    def _check_timer_recording_flag(timer_info, flag):
        timer_status = timer_info['status']
        if isinstance(timer_status, str):
            return int(timer_status) & flag
        return timer_status & flag

    def test(self):
        self.svdrp.connect()
        self.svdrp.send_cmd("LSTE 6 now")
        return self.svdrp.get_response_text()

    def finish(self):
        self.svdrp.shutdown()

    def mypyvdr(self):
        return (u'blubb')
