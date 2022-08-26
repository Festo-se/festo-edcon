"""Contains tests for EDriveMotion"""
from edrive.edrive_motion import EDriveMotion


def test_edrive_motion_over_v():
    """Tests the EDriveMotion class"""
    edpos = EDriveMotion()
    assert edpos.tg111.override.value == 16384
    edpos.over_v = 50.0
    assert edpos.tg111.override.value == 8192
