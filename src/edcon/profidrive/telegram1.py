"""Contains code that is related to PROFIDRIVE telegram 1"""

from dataclasses import dataclass, field
from edcon.profidrive.telegram_base import TelegramBase
from edcon.profidrive.words import STW1_SM, ZSW1_SM, NSOLL_A, NIST_A


@dataclass(repr=False)
class Telegram1(TelegramBase):
    """Holds the implementation of PROFIDRIVE telegram 1"""

    stw1: STW1_SM = field(default_factory=STW1_SM)
    nsoll_a: NSOLL_A = field(default_factory=NSOLL_A)

    zsw1: ZSW1_SM = field(default_factory=ZSW1_SM)
    nist_a: NIST_A = field(default_factory=NIST_A)

    def inputs(self):
        """Returns list of input words"""
        return [self.zsw1, self.nist_a]

    def outputs(self):
        """Returns list of output words"""
        return [self.stw1, self.nsoll_a]
