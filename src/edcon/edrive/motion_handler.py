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
    over_v = property(fset=lambda self, value: setattr(
        self.telegram, 'override',
        OVERRIDE(int(16384*(value/100.0)))), doc="Override velocity in percent")

    over_acc = property(fset=lambda self, value: setattr(
        self.telegram, 'mdi_acc',
        MDI_ACC(int(16384*(value/100.0)))), doc="Override acceleration in percent")

    over_dec = property(fset=lambda self, value: setattr(
        self.telegram, 'mdi_dec',
        MDI_DEC(int(16384*(value/100.0)))), doc="Override deceleration in percent")

    def __init__(self, edrive: ComBase = None) -> None:
        super().__init__(edrive)
        self.over_v = 100.0
        self.over_acc = 100.0
        self.over_dec = 100.0

        self.base_velocity = 0

    def scaled_velocity(self) -> int:
        """Convert the raw velocity to a scaled velocity
        """
        raw_velocity = self.telegram.nist_b
        return raw_velocity * self.base_velocity / 1073741824.0

    def current_velocity(self):
        """Read the current velocity

        Returns:
            int/float: In order to get the correct velocity, base_velocity needs to be provided.
                 If no base_velocity is given, returned value is raw and can be converted using
                 the following formula:

                 base_velocity = Base Value Velocity (parameterized on device)

                 current_velocity = raw_value * base_value_velocity / 0x40000000.
        """
        # self.update_inputs()
        if self.base_velocity > 0:
            return self.scaled_velocity()
        else:
            return self.telegram.nist_b
