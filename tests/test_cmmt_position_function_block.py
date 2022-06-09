"""Contains tests for CmmtPositionFunctionBlock"""
from eip_cmmt.cmmt_position_function_block import CmmtPositionFunctionBlock


def test_cmmt_position_function_block_over_v():
    """Tests the CmmtPositionFunctionBlock class"""
    fblock = CmmtPositionFunctionBlock()
    assert fblock.tg111.override.value == 16384
    fblock.over_v = 50.0
    assert fblock.tg111.override.value == 8192
