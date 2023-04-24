"""Contains tests for MotionHandler class"""
from edcon.cli.position import add_position_parser
from unittest.mock import Mock


class TestCli:
    def test_add_position_parser(self):
        parser = Mock()
        add_position_parser(parser)
        parser.add_parser.assert_called_with('position')
