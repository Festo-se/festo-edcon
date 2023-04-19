from profidrive.telegram102 import Telegram102
from edrive.telegram_executors.velocity_telegram_executor import VelocityTelegramExecutor


class Telegram102Executor(VelocityTelegramExecutor):
    """Basic class for executing telegram 1."""

    def __init__(self, edrive) -> None:
        super().__init__(Telegram102(), edrive)
        self.edrive.assert_selected_telegram(102)

    def prepare_velocity_task(self, velocity: int):
        self.telegram.nsoll_b.value = velocity

    def velocity_info(self) -> str:
        return f"Velocity [Target, Current]: " \
            f"[{int(self.telegram.nsoll_b)}, {int(self.telegram.nist_b)}]"
