"""Tests for cut."""

import os


def test_entrypoint() -> None:
    """Test that the command is recognised."""
    exit_status = os.system("cccut --help")
    assert exit_status == 0
