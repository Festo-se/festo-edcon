"""Contains code that is related to PROFIDRIVE words"""

from profidrive.words import BitwiseWordGeneric, IntWord, IntDoubleWord

# Test BitwiseWordGeneric


def test_bitwise_word_repr():
    """Test for BitwiseWordGeneric __repr__ method"""
    bwg = BitwiseWordGeneric()
    assert str(bwg) == \
        "BitwiseWordGeneric(bit0=False, bit1=False, bit2=False, bit3=False, bit4=False, "\
        "bit5=False, bit6=False, bit7=False, bit8=False, bit9=False, bit10=False, bit11=False, "\
        "bit12=False, bit13=False, bit14=False, bit15=False)"
    bwg.bit0 = True
    assert str(bwg) == \
        "BitwiseWordGeneric(bit0=True, bit1=False, bit2=False, bit3=False, bit4=False, "\
        "bit5=False, bit6=False, bit7=False, bit8=False, bit9=False, bit10=False, bit11=False, "\
        "bit12=False, bit13=False, bit14=False, bit15=False)"


def test_bitwise_word_int():
    """Test for BitwiseWordGeneric __int__ method"""
    assert int(BitwiseWordGeneric.from_bytes(b'\xab\xcd')) == 52651


def test_bitwise_word_generic_from_bytes():
    """Test for BitwiseWordGeneric from_bytes method"""
    bwg = BitwiseWordGeneric.from_bytes(b'\xab\xcd')
    assert str(bwg) == \
        "BitwiseWordGeneric(bit0=True, bit1=True, bit2=False, bit3=True, bit4=False, bit5=True, " \
        "bit6=False, bit7=True, bit8=True, bit9=False, bit10=True, bit11=True, bit12=False, " \
        "bit13=False, bit14=True, bit15=True)"


def test_bitwise_word_to_bytes():
    """Test for BitwiseWordGeneric to_bytes method"""
    bwg = BitwiseWordGeneric.from_bytes(b'\xab\xcd')
    bwg.bit0 = False
    assert bwg.to_bytes() == b'\xaa\xcd'


# Test IntWord
def test_int_word_int():
    """Test for IntWord __int__ method"""
    assert int(IntWord(12345)) == 12345


def test_int_word_from_bytes():
    """Test for IntWord from_bytes method"""
    intw = IntWord.from_bytes(b'\x00\x01')
    assert str(intw) == "IntWord(value=256, byte_size=2)"
    intw = IntWord.from_bytes(b'\xab\xcd')
    assert str(intw) == "IntWord(value=-12885, byte_size=2)"

# Test IntDoubleWord


def test_int_double_word_int():
    """Test for IntDoubleWord __int__ method"""
    assert int(IntDoubleWord(123456)) == 123456


def test_int_double_word_from_bytes():
    """Test for IntDoubleWord from_bytes method"""
    idw = IntDoubleWord.from_bytes(b'\x00\x01\x00\x00')
    assert str(idw) == "IntDoubleWord(value=256, byte_size=4)"

    idw = IntDoubleWord.from_bytes(b'\x00\x01\x00\x01')
    assert str(idw) == "IntDoubleWord(value=16777472, byte_size=4)"

    idw = IntDoubleWord.from_bytes(b'\xab\xcd\x00\x00')
    assert str(idw) == "IntDoubleWord(value=52651, byte_size=4)"
