"""Contains tests for all telegrams"""
from dataclasses import dataclass, field
import struct

from profidrive.telegram_base import TelegramBase
from profidrive.telegram1 import Telegram1
from profidrive.telegram102 import Telegram102
from profidrive.telegram111 import Telegram111
from profidrive.words import BitwiseWordGeneric, IntDoubleWord


@dataclass(repr=False)
class TelegramBaseTester(TelegramBase):
    """This is a test derivative of TelegramBase to test it's methods"""
    word1: BitwiseWordGeneric = field(default_factory=BitwiseWordGeneric)
    word2: IntDoubleWord = field(default_factory=IntDoubleWord)
    word3: BitwiseWordGeneric = field(default_factory=BitwiseWordGeneric)
    word4: BitwiseWordGeneric = field(default_factory=BitwiseWordGeneric)
    word5: BitwiseWordGeneric = field(default_factory=BitwiseWordGeneric)


class TestTelegramBase:
    def test_repr(self):
        """Test for TelegramBase __repr__ method"""
        tbt = TelegramBaseTester(0xDEAD, 0xBEEF, 0xBAAD, 0xBAAD, 0xF00D)
        assert str(tbt) == "TelegramBaseTester" \
            "(WORD1=0xDEAD, WORD2=0x0000BEEF, WORD3=0xBAAD, WORD4=0xBAAD, WORD5=0xF00D)"
        tbt = TelegramBaseTester()
        assert str(tbt) == "TelegramBaseTester" \
            "(WORD1=0x0000, WORD2=0x00000000, WORD3=0x0000, WORD4=0x0000, WORD5=0x0000)"
        tbt.word1.bit0 = True
        assert str(tbt) == "TelegramBaseTester" \
            "(WORD1=0x0001, WORD2=0x00000000, WORD3=0x0000, WORD4=0x0000, WORD5=0x0000)"

    def test_len(self):
        """Test for TelegramBase __len__ method"""
        assert len(TelegramBaseTester(
            0xDEAD, 0xBEEF, 0xBAAD, 0xBAAD, 0xF00D)) == 12


class TestTelegram1:
    def test_repr(selff):
        """Test for Telegram1 __repr__ method"""
        tg1 = Telegram1(0xDEAD, 0xBEEF, 0xBAAD, 0xF00D)
        assert str(tg1) == \
            "Telegram1(STW1=0xDEAD, NSOLL_A=0xBEEF, ZSW1=0xBAAD, NIST_A=0xF00D)"

    def test_init(self):
        """Test for Telegram1 __init__ method"""
        tg1 = Telegram1(0xDEAD, 0xBEEF, 0xBAAD, 0xF00D)
        assert int(tg1.stw1) == 0xDEAD
        assert int(tg1.nsoll_a) == struct.unpack('>h', b'\xBE\xEF')[0]
        assert int(tg1.zsw1) == 0xBAAD
        assert int(tg1.nist_a) == struct.unpack('>h', b'\xF0\x0D')[0]

    def test_output_bytes(self):
        """Test for Telegram1 output_bytes method"""
        tg1 = Telegram1(0xDEAD, 0xBEEF, 0xBAAD, 0xF00D)
        assert tg1.output_bytes() == bytes([0xAD, 0xDE, 0xEF, 0xBE])

    def test_input_bytes(self):
        """Test for Telegram1 input_bytes method"""
        tg1 = Telegram1()
        tg1.input_bytes(bytes([0xBA, 0xAD, 0xF0, 0x0D]))
        assert int(tg1.zsw1) == 0xADBA
        assert int(tg1.nist_a) == struct.unpack('>h', b'\x0D\xF0')[0]


class TestTelegram102:
    def test_repr(self):
        """Test for Telegram102 __repr__ method"""
        t102 = Telegram102(0xDEAD, 0xBEEF, 0xBAAD, 0xBAAD, 0xF00D)
        assert str(t102) == \
            "Telegram102(STW1=0xDEAD, NSOLL_B=0x0000BEEF, STW2=0xBAAD, MOMRED=0xBAAD, " \
            "G1_STW=0xF00D, ZSW1=0x0000, NIST_B=0x00000000, ZSW2=0x0000, MELDW=0x0000, " \
            "G1_ZSW=0x0000, G1_XIST1=0x00000000, G1_XIST2=0x00000000)"


class TestTelegram111:
    def test_repr(self):
        """Test for Telegram111 __repr__ method"""
        t111 = Telegram111()
        assert str(t111) == \
            "Telegram111(STW1=0x0000, POS_STW1=0x0000, POS_STW2=0x0000, STW2=0x0000, " \
            "OVERRIDE=0x0000, MDI_TARPOS=0x00000000, MDI_VELOCITY=0x00000000, MDI_ACC=0x0000, " \
            "MDI_DEC=0x0000, ZSW1=0x0000, POS_ZSW1=0x0000, POS_ZSW2=0x0000, ZSW2=0x0000, " \
            "MELDW=0x0000, XIST_A=0x00000000, NIST_B=0x00000000, FAULT_CODE=0x0000, WARN_CODE=0x0000)"
