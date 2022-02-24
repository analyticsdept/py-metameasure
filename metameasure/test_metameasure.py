from metameasure import MetaMeasure
import unittest

class TestMetaMeasure(unittest.TestCase):
    def setUp(self):
        self.m = MetaMeasure(max_size_bytes=10000, reset_when_threshold_exceeded=True)

    def test_byte_measure(self):
        d = {}
        self.assertEqual(self.m.measure(d), 64)

    def test_max_bytes(self):
        self.assertEqual(self.m.max_size_bytes, 10000)
    
    def test_reset_when_threshold_exceeded(self):
        self.assertEqual(self.m.reset_when_threshold_exceeded, True)

    def test_kb_to_bytes(self):
        expected = 1000
        self.assertEqual(expected, self.m.bytes(kb=1))

    def test_mb_to_bytes(self):
        expected = 1000000
        self.assertEqual(expected, self.m.bytes(mb=1))

    def test_gb_to_bytes(self):
        expected = 1000000000
        self.assertEqual(expected, self.m.bytes(gb=1))

    def test_tb_to_bytes(self):
        expected = 1000000000000
        self.assertEqual(expected, self.m.bytes(tb=1))

    

if __name__ == "__main__":
    unittest.main()