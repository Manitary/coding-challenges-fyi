"""Tests for cut."""

import os
from pathlib import Path
import cut


def test_entrypoint() -> None:
    """Test that the command is recognised."""
    exit_status = os.system("cccut --help")
    assert exit_status == 0


def test_cut_one_field_tsv(cut_sample_tsv: Path) -> None:
    """Test cutting one field of a tsv file."""
    result = cut.cut_fields(cut_sample_tsv, fields=[2])
    expected = "f1\n1\n6\n11\n16\n21"
    assert result == expected


def test_cut_two_fields_tsv(cut_sample_tsv: Path) -> None:
    """Test cutting two fields of a tsv file."""
    result = cut.cut_fields(cut_sample_tsv, fields=[1, 2])
    expected = "f0\tf1\n0\t1\n5\t6\n10\t11\n15\t16\n20\t21"
    assert result == expected
