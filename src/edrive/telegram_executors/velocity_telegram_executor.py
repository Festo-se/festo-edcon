import logging
from edrive.telegram_executors.telegram_executor import TelegramExecutor


class VelocityTelegramExecutor(TelegramExecutor):
    """Basic class for executing velocity telegrams."""

    def __init__(self, telegram, edrive) -> None:
        super().__init__(telegram, edrive)

        # Set default bits for velocity telegrams
        self.telegram.stw1.enable_ramp_generator = True
        self.telegram.stw1.unfreeze_ramp_generator = True

    def stop_motion_task(self):
        """Stops any currently active motion task"""
        logging.info("Stopping motion")
        self.telegram.stw1.setpoint_enable = False
        self.update_outputs()

    def velocity_task(self, velocity: int, duration: float = 0.0) -> bool:
        if not self.ready_for_motion():
            return False
        logging.info("Start velocity task")

        self.prepare_velocity_task(velocity)
        self.telegram.stw1.setpoint_enable = True
        self.update_outputs()

        if duration == 0:
            return True

        # Wait for predefined amount of time

        if not self.wait_for_duration(duration, self.velocity_info):
            return False

        self.stop_motion_task()
        logging.info("Finished velocity task")
        return True
