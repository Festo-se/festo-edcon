"""Class definition containing telegram 9 execution functions."""

from edcon.edrive.position_telegram_handler import PositionTelegramHandler
from edcon.profidrive.telegram9 import Telegram9
from edcon.edrive.parameter_handler import ParameterHandler
from edcon.edrive.parameter import Parameter


class Telegram9Handler(PositionTelegramHandler):
    """Basic class for executing telegram 9.

    Parameters:
        com (ComBase): communication driver
        config_mode (str): configuration mode (None, "write", "validate")
    """

    def __init__(self, com, config_mode=None) -> None:
        if config_mode == "write":
            ParameterHandler(com).write(Parameter.from_uid("P0.3030101.0.0", 9))
        elif config_mode == "validate":
            ParameterHandler(com).validate("P0.3030101.0.0", 9)
        super().__init__(Telegram9(), com)

    def _prepare_position_task_bits(
        self, position: int, velocity: int, absolute: bool = False
    ):
        """Prepares the telegram bits for positioning task"""
        super()._prepare_position_task_bits(position, velocity, absolute)
        self.telegram.satzanw.mdi_active = True
        self.telegram.mdi_mod.absolute_position = absolute
