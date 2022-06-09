"""Contains tests for boollist"""
from eip_cmmt.utils.boollist import bytes_to_boollist, boollist_to_bytes

# Test bytes_to_boollist


def test_bytes_to_boollist_8bit():
    """Tests the function bytes_to_boollist with 8 bits"""
    assert bytes_to_boollist(b'\xa5') == [
        True, False, True, False, False, True, False, True]


def test_bytes_to_boollist_8bit_to_16bit():
    """Tests the function bytes_to_boollist with 8 bits but outputting 16 bits"""
    assert bytes_to_boollist(b'\xa5', 2) == [True, False, True, False, False, True, False, True,
                                             False, False, False, False, False, False, False, False]


def test_bytes_to_boollist_16bit():
    """Tests the function bytes_to_boollist with 16 bits"""
    assert bytes_to_boollist(b'\xa5Z') == [True, False, True, False, False, True, False, True,
                                           False, True, False, True, True, False, True, False]
    assert bytes_to_boollist(b'\xab\xcd') == [True, True, False, True, False, True, False, True,
                                              True, False, True, True, False, False, True, True]


def test_bytes_to_boollist_16bit_to_8bit():
    """Tests the function bytes_to_boollist with 16 bits but outputting 8 bits"""
    assert bytes_to_boollist(b'\xa5Z', 1) == [
        True, False, True, False, False, True, False, True]


def test_bytes_to_boollist_32bit():
    """Tests the function bytes_to_boollist with 32 bits"""
    assert bytes_to_boollist(b'\xa5Z\xa5Z') == [True, False, True, False, False, True, False,
                                                True, False, True, False, True, True, False,
                                                True, False, True, False, True, False, False,
                                                True, False, True, False, True, False, True,
                                                True, False, True, False]

# Test boollist_to_bytes


def test_boollist_to_bytes_8bit():
    """Tests the function boollist_to_bytes with 8 bits"""
    assert boollist_to_bytes(
        [True, False, True, False, False, True, False, True]) == b'\xa5'


def test_boollist_to_bytes_16bit():
    """Tests the function boollist_to_bytes with 16 bits"""
    assert boollist_to_bytes([True, False, True, False, False, True, False, True,
                              False, True, False, True, True, False, True, False]) == b'\xa5Z'
