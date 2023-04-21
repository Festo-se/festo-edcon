"""Contains tests for MotionExecutor class"""
from edcon.edrive.motion import MotionExecutor
from unittest.mock import Mock, call


class TestMotionExecutor:
    def test_over_v(self):
        """Tests over_v property"""
        edrive = Mock()
        mot = MotionExecutor(edrive)
        assert mot.telegram.override.value == 16384
        mot.over_v = 50.0
        assert mot.telegram.override.value == 8192
