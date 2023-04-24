"""
Contains MotionHandler class to configure and control
EDrive devices in position mode.
"""
from edcon.profidrive.words import OVERRIDE, MDI_ACC, MDI_DEC
from edcon.edrive.com_base import ComBase
from edcon.edrive.telegram111_handler import Telegram111Handler


class MotionHandler(Telegram111Handler):
    """
    This class is used to control the EDrive devices in position mode (telegram 111).
    It provides a set of functions to control the position of the EDrive using different modes.
    """

    def __init__(self, edrive: ComBase = None) -> None:
        super().__init__(edrive)
        self.over_v = 100.0
        self.over_acc = 100.0
        self.over_dec = 100.0
        self.base_velocity = 0

    @property
    def over_v(self):
        """Override velocity in percent"""
        return 100.0 * self.telegram.override.value / 0x4000

    @over_v.setter
    def over_v(self, value):
        self.telegram.override = OVERRIDE(int(0x4000*(value/100.0)))

    @property
    def over_acc(self):
        """Override acceleration in percent"""
        return 100.0 * self.telegram.mdi_acc.value / 0x4000

    @over_acc.setter
    def over_acc(self, value):
        self.telegram.mdi_acc = MDI_ACC(int(0x4000*(value/100.0)))

    @property
    def over_dec(self):
        """Override deceleration in percent"""
        return 100.0 * self.telegram.mdi_dec.value / 0x4000

    @over_dec.setter
    def over_dec(self, value):
        self.telegram.mdi_dec = MDI_DEC(int(0x4000*(value/100.0)))

    @property
    def scaled_velocity(self):
        """Velocity scaled to base velocity"""
        return self.telegram.nist_b.value * self.base_velocity / 0x40000000

    def current_velocity(self):
        """Read the current velocity

        Returns:
            int/float: In order to get the correct velocity, base_velocity needs to be provided.
                 If no base_velocity is given, returned value is raw and can be converted using
                 the following formula:

                 base_velocity = Base Value Velocity (parameterized on device)

                 current_velocity = raw_value * base_value_velocity / 0x40000000.
        """
        self.update_inputs()
        if self.base_velocity > 0:
            return self.scaled_velocity
        return self.telegram.nist_b
