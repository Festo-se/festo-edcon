"""Contains tests for MotionHandler class"""
from edcon.utils.func_helpers import func_sequence
from unittest.mock import Mock, call


class TestFuncHelpers:
    def test_pulse_bit_high_low(self):
        """Tests high pulse bit toggling"""
        toggle_func = Mock()
        func_sequence(toggle_func, [True, False])

        # Check if toggle function was called with correct value
        toggle_func.assert_has_calls([call(True), call(False)])

    def test_pulse_bit_active_low(self):
        """Tests low pulse bit toggling"""
        toggle_func = Mock()
        func_sequence(toggle_func, [False, True])

        # Check if toggle function was called with correct value
        toggle_func.assert_has_calls([call(False), call(True)])
