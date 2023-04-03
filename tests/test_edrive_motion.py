"""Contains tests for EDriveMotion class"""
from edrive.edrive_motion import EDriveMotion
from unittest.mock import Mock, call


class TestEDriveMotion:
    def test_over_v(self):
        """Tests over_v property"""
        mot = EDriveMotion()
        assert mot.tg111.override.value == 16384
        mot.over_v = 50.0
        assert mot.tg111.override.value == 8192

    def test_pulse_bit_active_high(self):
        """Tests high pulse bit toggling"""
        edrive = Mock()
        mot = EDriveMotion(edrive)

        toggle_func = Mock()
        active_high = True
        mot.pulse_bit(toggle_func, active_high)

        # Check if toggle function was called with correct value
        toggle_func.assert_has_calls([call(True), call(False)])

    def test_pulse_bit_active_low(self):
        """Tests low pulse bit toggling"""
        edrive = Mock()
        mot = EDriveMotion(edrive)

        toggle_func = Mock()
        active_high = False
        mot.pulse_bit(toggle_func, active_high)

        # Check if toggle function was called with correct value
        toggle_func.assert_has_calls([call(False), call(True)])
