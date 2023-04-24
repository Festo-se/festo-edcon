"""Contains tests for MotionHandler class"""
import time
from edcon.utils.func_helpers import func_sequence, wait_until, wait_for
from unittest.mock import Mock, call
from pytest import approx


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

    def test_wait_until_instant_return_true(self):
        """Tests wait_until with instant True condition"""
        def cond():
            return True
        res = wait_until(cond)

        assert res == True

    def test_wait_until_eventually_return_true(self):
        """Tests wait_until with True condition after few calls"""
        cond = Mock(side_effect=[False, False, True])

        res = wait_until(cond)

        assert cond.call_count == 3
        assert res == True

    def test_wait_until_error_condition_return_false(self):
        """Tests wait_until with True error condition"""
        def cond():
            return False

        def err_cond():
            return True
        res = wait_until(cond, err_cond, timeout=0.1)

        assert res == False

    def test_wait_until_timeout_return_false(self):
        """Tests wait_until with timeout"""
        def cond():
            return False
        start_time = time.time()
        res = wait_until(cond, timeout=0.1)
        elapsed_time = time.time() - start_time

        assert res == False
        assert elapsed_time == approx(0.1, 0.01)

    def test_wait_for_timeout_return_true(self):
        """Tests wait_for and return True after specified time"""
        start_time = time.time()
        res = wait_for(0.1)
        elapsed_time = time.time() - start_time

        assert res == True
        assert elapsed_time == approx(0.1, 0.01)

    def test_wait_for_error_condition_return_false(self):
        """Tests wait_for"""
        def err_cond():
            return True
        start_time = time.time()
        res = wait_for(0.1, err_cond)
        elapsed_time = time.time() - start_time

        assert res == False
        assert elapsed_time == approx(0.0, 0.01)
