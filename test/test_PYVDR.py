import unittest
from pyvdr import pyvdr as p


class TestPYVDR(unittest.TestCase):
    def setUp(self):
        self.func = p.PYVDR()

    def test__parse_channel_response(self):
        chan_no_1, chan_name_ARD = p.PYVDR._parse_channel_response("1 ARD")
        self.assertEquals(chan_no_1, "1")
        self.assertEquals(chan_name_ARD, "ARD")
        chan_no_11, chan_name_Prosieben = p.PYVDR._parse_channel_response("11 Prosieben")
        self.assertEquals(chan_no_11, "11")
        self.assertEquals(chan_name_Prosieben, "Prosieben")

    def test__check_timer_recording_flag(self):
        t_active = p.timer_info(Status=1, Name="Test1", Description="Description1", Date="2018-08-01")
        t_inactive = p.timer_info(Status=1, Name="Test1", Description="Description1", Date="2018-08-01")
        t_active_and_recording = p.timer_info(Status=9, Name="t_active_and_recording", Description="Description1", Date="2018-08-01")
        t_active_and_instant_recording = p.timer_info(Status=11, Name="t_active_and_instantrecording", Description="Description1", Date="2018-08-01")

        # timer active, not yet recording
        self.assertTrue(p.PYVDR._check_timer_recording_flag(t_active, p.FLAG_TIMER_ACTIVE), "Timer should be active")
        self.assertFalse(p.PYVDR._check_timer_recording_flag(t_active, p.FLAG_TIMER_RECORDING), "Timer should not be recording")

        # timer active, recording
        self.assertTrue(p.PYVDR._check_timer_recording_flag(t_active_and_recording, p.FLAG_TIMER_ACTIVE), "Timer should be active")
        self.assertTrue(p.PYVDR._check_timer_recording_flag(t_active_and_recording, p.FLAG_TIMER_RECORDING), "Timer should be recording")

        # instant recording
        self.assertTrue(p.PYVDR._check_timer_recording_flag(t_active_and_instant_recording, p.FLAG_TIMER_RECORDING), "Timer active")
        self.assertTrue(p.PYVDR._check_timer_recording_flag(t_active_and_instant_recording, p.FLAG_TIMER_RECORDING), "Timer recording")
        self.assertTrue(p.PYVDR._check_timer_recording_flag(t_active_and_instant_recording, p.FLAG_TIMER_INSTANT_RECORDING), "Timer instant recording")


if __name__ == '__main__':
    unittest.main()