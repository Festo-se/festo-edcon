"""
Contains MotionExecutor class to configure and control
EDrive devices in position mode.
"""
from edcon.profidrive.words import OVERRIDE, MDI_ACC, MDI_DEC
from edcon.edrive.com_base import ComBase
from edcon.edrive.telegram_executors.telegram111_executor import Telegram111Executor


class MotionExecutor(Telegram111Executor):
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

    def scaled_velocity(self, raw_velocity: int) -> int:
        """Convert the raw velocity to a scaled velocity

        Parameters:
            raw_velocity (int): raw velocity to convert to scaled
        """
        return raw_velocity * self.base_velocity / 1073741824.0 \
            if self.base_velocity > 0 else raw_velocity

# Reading current values
    def current_velocity(self):
        """Read the current velocity

        Returns:
            int/float: In order to get the correct velocity, base_velocity needs to be provided.
                 If no base_velocity is given, returned value is raw and can be converted using
                 the following formula:

                 base_value_velocity = Base Value Velocity (parameterized on device)

                 current_velocity = raw_value * base_value_velocity / 0x40000000.
        """
        self.update_inputs()
        return self.scaled_velocity(self.telegram.nist_b.value)
