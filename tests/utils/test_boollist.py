"""Contains tests for boollist"""
from edcon.utils.boollist import bytes_to_boollist, boollist_to_bytes


class TestBytesToBoollist:
    def test_8bit(self):
        """Tests the function bytes_to_boollist with 8 bits"""
        assert bytes_to_boollist(b'\xa5') == [
            True, False, True, False, False, True, False, True]

    def test_8bit_to_16bit(self):
        """Tests the function bytes_to_boollist with 8 bits but outputting 16 bits"""
        assert bytes_to_boollist(b'\xa5', 2) == [True, False, True, False, False, True, False, True,
                                                 False, False, False, False, False, False, False, False]

    def test_16bit(self):
        """Tests the function bytes_to_boollist with 16 bits"""
        assert bytes_to_boollist(b'\xa5Z') == [True, False, True, False, False, True, False, True,
                                               False, True, False, True, True, False, True, False]
        assert bytes_to_boollist(b'\xab\xcd') == [True, True, False, True, False, True, False, True,
                                                  True, False, True, True, False, False, True, True]

    def test_16bit_to_8bit(self):
        """Tests the function bytes_to_boollist with 16 bits but outputting 8 bits"""
        assert bytes_to_boollist(b'\xa5Z', 1) == [
            True, False, True, False, False, True, False, True]

    def test_32bit(self):
        """Tests the function bytes_to_boollist with 32 bits"""
        assert bytes_to_boollist(b'\xa5Z\xa5Z') == [True, False, True, False, False, True, False,
                                                    True, False, True, False, True, True, False,
                                                    True, False, True, False, True, False, False,
                                                    True, False, True, False, True, False, True,
                                                    True, False, True, False]


class TestBoollistToBytes:
    def test_8bit(self):
        """Tests the function boollist_to_bytes with 8 bits"""
        assert boollist_to_bytes(
            [True, False, True, False, False, True, False, True]) == b'\xa5'

    def test_16bit(self):
        """Tests the function boollist_to_bytes with 16 bits"""
        assert boollist_to_bytes([True, False, True, False, False, True, False, True,
                                  False, True, False, True, True, False, True, False]) == b'\xa5Z'
