import unittest
from pyvdr import PYVDR


class TestPYVDR(unittest.TestCase):
    def setUp(self):
        self.func = PYVDR()

    def test__parse_channel_response(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()