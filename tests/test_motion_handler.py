"""Contains tests for MotionHandler class"""
from edcon.edrive.motion_handler import MotionHandler
from unittest.mock import Mock


class TestMotionHandler:
    def test_over_v(self):
        """Tests over_v property"""
        edrive = Mock()
        mot = MotionHandler(edrive)
        assert mot.telegram.override.value == 16384
        mot.over_v = 50.0
        assert mot.telegram.override.value == 8192

    def test_over_v_multiple_instances(self):
        """Tests over_v property"""
        edrive = Mock()
        mot = MotionHandler(edrive)
        assert mot.telegram.override.value == 16384

        mot2 = MotionHandler(edrive)
        assert mot2.telegram.override.value == 16384

        mot.over_v = 50.0
        mot2.over_v = 25.0
        assert mot.telegram.override.value == 8192
        assert mot2.telegram.override.value == 4096

    def test_over_acc(self):
        """Tests over_acc property"""
        edrive = Mock()
        mot = MotionHandler(edrive)
        assert mot.telegram.mdi_acc.value == 16384
        mot.over_acc = 50.0
        assert mot.telegram.mdi_acc.value == 8192

    def test_over_dec(self):
        """Tests over_dec property"""
        edrive = Mock()
        mot = MotionHandler(edrive)
        assert mot.telegram.mdi_dec.value == 16384
        mot.over_dec = 50.0
        assert mot.telegram.mdi_dec.value == 8192

    def test_scaled_velocity(self):
        """Tests scaled_velocity"""
        edrive = Mock()
        mot = MotionHandler(edrive)
        mot.base_velocity = 1000
        mot.telegram.nist_b = 2000

        assert mot.scaled_velocity() == 2000 * (1000 / 0x40000000)
