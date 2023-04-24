"""Contains tests for MotionHandler class"""
from edcon.edrive.motion_handler import MotionHandler
from unittest.mock import Mock, call


class TestMotionHandler:
    def test_over_v(self):
        """Tests over_v property"""
        edrive = Mock()
        mot = MotionHandler(edrive)
        assert mot.telegram.override.value == 16384
        mot.over_v = 50.0
        assert mot.telegram.override.value == 8192
