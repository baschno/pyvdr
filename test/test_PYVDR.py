import unittest
from unittest.mock import MagicMock
from pyvdr import PYVDR
from pyvdr import pyvdr


class TestPYVDR(unittest.TestCase):
    def setUp(self):
        self.func = PYVDR()
        self.func.stat = MagicMock( return_value = 3)

    def test__parse_channel_response(self):
        chan_ard = self.func._parse_channel_response(["", "","1 ARD"])
        self.assertEqual(chan_ard.Number, "1")
        self.assertEqual(chan_ard.Name, "ARD")

        chan_prosieben = self.func._parse_channel_response(["", "","11 Pro Sieben"])
        self.assertEqual(chan_prosieben.Number, "11")
        self.assertEqual(chan_prosieben.Name, "Pro Sieben")

    def test__check_timer_recording_flag(self):
        t_active = pyvdr.timer_info(Status=1, Name="Test1", Description="Description1", Date="2018-08-01")
        t_inactive = pyvdr.timer_info(Status=1, Name="Test1", Description="Description1", Date="2018-08-01")
        t_active_and_recording = pyvdr.timer_info(Status=9, Name="t_active_and_recording", Description="Description1", Date="2018-08-01")
        t_active_and_instant_recording = pyvdr.timer_info(Status=11, Name="t_active_and_instantrecording", Description="Description1", Date="2018-08-01")

        # timer active, not yet recording
        self.assertTrue(self.func._check_timer_recording_flag(t_active, pyvdr.FLAG_TIMER_ACTIVE), "Timer should be active")
        self.assertFalse(self.func._check_timer_recording_flag(t_active, pyvdr.FLAG_TIMER_RECORDING), "Timer should not be recording")

        # timer active, recording
        self.assertTrue(self.func._check_timer_recording_flag(t_active_and_recording, pyvdr.FLAG_TIMER_ACTIVE), "Timer should be active")
        self.assertTrue(self.func._check_timer_recording_flag(t_active_and_recording, pyvdr.FLAG_TIMER_RECORDING), "Timer should be recording")

        # instant recording
        self.assertTrue(self.func._check_timer_recording_flag(t_active_and_instant_recording, pyvdr.FLAG_TIMER_RECORDING), "Timer active")
        self.assertTrue(self.func._check_timer_recording_flag(t_active_and_instant_recording, pyvdr.FLAG_TIMER_RECORDING), "Timer recording")
        self.assertTrue(self.func._check_timer_recording_flag(t_active_and_instant_recording, pyvdr.FLAG_TIMER_INSTANT_RECORDING), "Timer instant recording")


if __name__ == '__main__':
    unittest.main()