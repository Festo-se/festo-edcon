"""Contains tests for EDrivePositioning"""
from edrive.edrive_positioning import EDrivePositioning


def test_edrive_positioning_over_v():
    """Tests the EDrivePositioning class"""
    edpos = EDrivePositioning()
    assert edpos.tg111.override.value == 16384
    edpos.over_v = 50.0
    assert edpos.tg111.override.value == 8192
