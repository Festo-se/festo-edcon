"""Class definition containing telegram 9 execution functions."""

from edcon.edrive.telegram_executors.position_telegram_executor import PositionTelegramExecutor
from edcon.profidrive.telegram9 import Telegram9


class Telegram9Executor(PositionTelegramExecutor):
    """Basic class for executing telegram 9."""

    def __init__(self, edrive) -> None:
        super().__init__(Telegram9(), edrive)
        self.edrive.validate_selected_telegram(9)

    def _prepare_position_task_bits(self, position: int, velocity: int, absolute: bool = False):
        """Prepares the telegram bits for positioning task"""
        super()._prepare_position_task_bits(position, velocity, absolute)
        self.telegram.satzanw.mdi_active = True
        self.telegram.mdi_mod.absolute_position = absolute
