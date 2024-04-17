"""Contains tests for MotionHandler class"""

from edcon.edrive.motion_handler import MotionHandler
from unittest.mock import Mock, MagicMock
from edcon.profidrive.words import NIST_B


class TestMotionHandler:
    def test_over_v_set(self):
        """Tests over_v property"""
        com = Mock()
        mot = MotionHandler(com)
        assert mot.telegram.override.value == 16384
        mot.over_v = 50.0
        assert mot.telegram.override.value == 8192

    def test_over_v_get(self):
        """Tests over_v property"""
        com = Mock()
        mot = MotionHandler(com)
        mot.telegram.override.value = 8192
        assert mot.over_v == 50.0

    def test_over_v_set_multiple_instances(self):
        """Tests over_v property"""
        com = Mock()
        mot = MotionHandler(com)
        assert mot.telegram.override.value == 16384

        mot2 = MotionHandler(com)
        assert mot2.telegram.override.value == 16384

        mot.over_v = 50.0
        mot2.over_v = 25.0
        assert mot.telegram.override.value == 8192
        assert mot2.telegram.override.value == 4096

    def test_over_acc(self):
        """Tests over_acc property"""
        com = Mock()
        mot = MotionHandler(com)
        assert mot.telegram.mdi_acc.value == 16384
        mot.over_acc = 50.0
        assert mot.telegram.mdi_acc.value == 8192

    def test_over_dec(self):
        """Tests over_dec property"""
        com = Mock()
        mot = MotionHandler(com)
        assert mot.telegram.mdi_dec.value == 16384
        mot.over_dec = 50.0
        assert mot.telegram.mdi_dec.value == 8192

    def test_current_velocity(self):
        """Tests current_velocity"""
        com = Mock()
        mot = MotionHandler(com)
        mot.update_inputs = Mock()

        mot.base_velocity = 1000
        mot.telegram.nist_b = NIST_B(2000)

        assert mot.current_velocity() == 2000 * (1000 / 0x40000000)
