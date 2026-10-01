"""Tests for parameter mapping."""

from edcon.edrive.parameter_mapping import read_pnu_map_file


def test_read_packaged_pnu_map_decodes_utf8():
    pnu_map = read_pnu_map_file()

    assert next(item for item in pnu_map if item.pnu == 2739).name == "Time constant I²t"