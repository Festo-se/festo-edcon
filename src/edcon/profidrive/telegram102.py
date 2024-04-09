"""Contains code that is related to PROFIDRIVE telegram 102"""

from dataclasses import dataclass, field
from edcon.profidrive.telegram_base import TelegramBase
from edcon.profidrive.words import (
    STW1_SM,
    NSOLL_B,
    STW2,
    MOMRED,
    G1_STW,
    ZSW1_SM,
    NIST_B,
    ZSW2,
    MELDW,
    G1_ZSW,
    G1_XIST1,
    G1_XIST2,
)


@dataclass(repr=False)
class Telegram102(TelegramBase):
    """Holds the implementation of PROFIDRIVE telegram 102"""

    # pylint: disable=too-many-instance-attributes
    # Twelve is needed here
    stw1: STW1_SM = field(default_factory=STW1_SM)
    nsoll_b: NSOLL_B = field(default_factory=NSOLL_B)
    stw2: STW2 = field(default_factory=STW2)
    momred: MOMRED = field(default_factory=MOMRED)
    g1_stw: G1_STW = field(default_factory=G1_STW)

    zsw1: ZSW1_SM = field(default_factory=ZSW1_SM)
    nist_b: NIST_B = field(default_factory=NIST_B)
    zsw2: ZSW2 = field(default_factory=ZSW2)
    meldw: MELDW = field(default_factory=MELDW)
    g1_zsw: G1_ZSW = field(default_factory=G1_ZSW)
    g1_xist1: G1_XIST1 = field(default_factory=G1_XIST1)
    g1_xist2: G1_XIST2 = field(default_factory=G1_XIST2)

    def inputs(self):
        """Returns list of input words"""
        return [
            self.zsw1,
            self.nist_b,
            self.zsw2,
            self.meldw,
            self.g1_zsw,
            self.g1_xist1,
            self.g1_xist2,
        ]

    def outputs(self):
        """Returns list of output words"""
        return [self.stw1, self.nsoll_b, self.stw2, self.momred, self.g1_stw]
