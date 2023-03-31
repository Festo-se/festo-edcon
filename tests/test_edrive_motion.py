"""Contains tests for EDriveMotion class"""
from edrive.edrive_motion import EDriveMotion
from unittest.mock import Mock


class TestEDriveMotion:
    def test_over_v(self):
        """Tests over_v property"""
        mot = EDriveMotion()
        assert mot.tg111.override.value == 16384
        mot.over_v = 50.0
        assert mot.tg111.override.value == 8192

    def test_pulse_bit_active_high(self):
        """Tests over_v property"""
        edrive = Mock()
        mot = EDriveMotion(edrive)

        set_bit_values = []

        def set_bit(value):
            set_bit_values.append(value)

        mot.pulse_bit(set_bit)

        assert set_bit_values == [True, False]

    def test_pulse_bit_active_low(self):
        """Tests over_v property"""
        edrive = Mock()
        mot = EDriveMotion(edrive)

        set_bit_values = []

        def set_bit(value):
            set_bit_values.append(value)

        mot.pulse_bit(set_bit, active_high=False)

        assert set_bit_values == [False, True]
