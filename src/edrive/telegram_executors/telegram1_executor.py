from profidrive.telegram1 import Telegram1
from edrive.telegram_executors.velocity_telegram_executor import VelocityTelegramExecutor


class Telegram1Executor(VelocityTelegramExecutor):
    """Basic class for executing telegram 1."""

    def __init__(self, edrive) -> None:
        super().__init__(Telegram1(), edrive)
        self.edrive.validate_selected_telegram(1)

    def prepare_velocity_task(self, velocity: int):
        self.telegram.nsoll_a.value = velocity

    def velocity_info(self) -> str:
        return f"Velocity [Target, Current]: " \
            f"[{int(self.telegram.nsoll_a)}, {int(self.telegram.nist_a)}]"
