#!/usr/bin/env python3

from .svdrp import SVDRP
from .svdrp import SVDRP_COMMANDS
from .svdrp import SVDRP_RESULT_CODE

import logging
import re
from collections import namedtuple

epg_info = namedtuple('EPGDATA', 'Channel Title Description')

FLAG_TIMER_ACTIVE = 1
FLAG_TIMER_INSTANT_RECORDING = 2
FLAG_TIMER_VPS = 4
FLAG_TIMER_RECORDING = 8

_LOGGER = logging.getLogger(__name__)


class PYVDR(object):

    def __init__(self, hostname='localhost', timeout=10):
        self.hostname = hostname
        self.svdrp = SVDRP(hostname=self.hostname, timeout=timeout)
        self.timers = None

    def stat(self):
        self.svdrp.send_cmd(SVDRP_COMMANDS.DISK_INFO)
        disk_stat_response = self.svdrp.get_response()[1:][0]

        if disk_stat_response.Code != SVDRP.SVDRP_STATUS_OK:
            return -1

        disk_stat_parts = re.match(
            r'(\d*)\w. (\d*)\w. (\d*)',
            disk_stat_response.Value, re.M | re.I)
        if disk_stat_parts:
            return [disk_stat_parts.group(1),
                    disk_stat_parts.group(2),
                    disk_stat_parts.group(3)]
        else:
            return None

    """
    Gets the channel info and returns the channel number and the channel name.
    """
    def get_channel(self):
        self.svdrp.send_cmd(SVDRP_COMMANDS.GET_CHANNEL)
        responses = self.svdrp.get_response()
        _LOGGER.debug("Response of get channel cmd: '%s'" % responses)
        if len(responses) < 1:
            return None
        # get 2nd element (1. welcome, 2. response, 3. quit msg)
        generic_response = responses[-2]
        channel = self._parse_channel_response(generic_response)
        _LOGGER.debug("Returned Chan: '%s'" % channel)
        return channel

    @staticmethod
    def _parse_channel_response(channel_data):
        _LOGGER.debug("Parsing Channel response to fields: %s" % channel_data.Value)
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
        timer_match = re.match(
            r'^(\d) (\d{1,2}):(\d{1,2}):(\d{4}-\d{2}-\d{2}):(\d{4}):(\d{4}):(\d+):(\d+):(.*):(.*)$',
            response.Value,
            re.M | re.I)

        if timer_match:
            timer['status'] = timer_match.group(2)
            timer['channel'] = timer_match.group(3)
            timer['date'] = timer_match.group(4)
            timer['name'] = timer_match.group(9)
            timer['description'] = ""
            timer['series'] = timer['name'].find('~') != -1
            timer['instant'] = False
            _LOGGER.debug("Parsed timer: {}".format(timer))
        else:
            _LOGGER.debug("You might want to check the regex for timer parsing?! {}".format(response))

        return timer

    def get_timers(self):
        timers = []
        self.svdrp.send_cmd(SVDRP_COMMANDS.LIST_TIMERS)
        responses = self.svdrp.get_response()
        for response in responses:
            if response.Code != SVDRP_RESULT_CODE.SUCCESS:
                continue
            timers.append(self._parse_timer_response(response))
        return timers

    def is_recording(self):
        self.svdrp.send_cmd(SVDRP_COMMANDS.LIST_TIMERS)
        responses = self.svdrp.get_response()
        for response in responses:
            if response.Code != SVDRP_RESULT_CODE.SUCCESS:
                continue
            timer = self._parse_timer_response(response)
            if len(timer) <= 0:
                _LOGGER.debug("No output from timer parsing.")
                return None
            if self._check_timer_recording_flag(timer, FLAG_TIMER_INSTANT_RECORDING):
                timer['instant'] = True
                return timer
            if self._check_timer_recording_flag(timer, FLAG_TIMER_RECORDING):
                return timer

        return None

    def get_channel_epg_info(self, channel_no=1):
        epg_title = epg_channel = epg_description = None
        self.svdrp.send_cmd(f"{SVDRP_COMMANDS.LIST_EPG} {channel_no} now")
        epg_data = self.svdrp.get_response()[1:]
        for data in epg_data:
            if data[0] == SVDRP_RESULT_CODE.EPG_DATA_RECORD:
                epg = re.match(r'^(\S)\s(.*)$', data[2], re.M | re.I)
                if epg is not None:
                    epg_field_type = epg.group(1)
                    epg_field_value = epg.group(2)

                    if epg_field_type == 'T':
                        epg_title = epg_field_value
                    if epg_field_type == 'C':
                        epg_channel = epg_field_value
                    if epg_field_type == 'D':
                        epg_description = epg_field_value

        return epg_info(
            Channel=epg_channel,
            Title=epg_title,
            Description=epg_description)

    def channel_up(self):
        self.svdrp.send_cmd(SVDRP_COMMANDS.CHANNEL_UP)
        response_text = self.svdrp.get_response_as_text()
        return response_text

    def channel_down(self):
        self.svdrp.send_cmd(SVDRP_COMMANDS.CHANNEL_DOWN)
        response_text = self.svdrp.get_response_as_text()
        return response_text

    def list_recordings(self):
        self.svdrp.send_cmd(SVDRP_COMMANDS.LIST_RECORDINGS)
        return self.svdrp.get_response()[1:]

    @staticmethod
    def _check_timer_recording_flag(timer_info, flag):
        timer_status = timer_info['status']
        if isinstance(timer_status, str):
            return int(timer_status) & flag
        return timer_status & flag
