"""Tests for cut."""

import os
from pathlib import Path
import pytest
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


def test_cut_one_field_cli(
    capfd: pytest.CaptureFixture[str], cut_sample_tsv: Path
) -> None:
    """Test cut -f 2."""
    exit_status = os.system(f"cccut -f2 {cut_sample_tsv}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == "f1\r\n1\r\n6\r\n11\r\n16\r\n21"


def test_cut_two_fields_tsv(cut_sample_tsv: Path) -> None:
    """Test cutting two fields of a tsv file."""
    result = cut.cut_fields(cut_sample_tsv, fields=[1, 2])
    expected = "f0\tf1\n0\t1\n5\t6\n10\t11\n15\t16\n20\t21"
    assert result == expected


def test_cut_two_fields_cli(
    capfd: pytest.CaptureFixture[str], cut_sample_tsv: Path
) -> None:
    """Test cut -f 2 3."""
    exit_status = os.system(f"cccut -f 1,2 {cut_sample_tsv}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert (
        captured.out.rstrip() == "f0\tf1\r\n0\t1\r\n5\t6\r\n10\t11\r\n15\t16\r\n20\t21"
    )


def test_cut_two_fields_cli_alt_syntax(
    capfd: pytest.CaptureFixture[str], cut_sample_tsv: Path
) -> None:
    """Test cut -f 2 3."""
    exit_status = os.system(f'cccut -f"1 2" {cut_sample_tsv}')
    captured = capfd.readouterr()
    assert exit_status == 0
    assert (
        captured.out.rstrip() == "f0\tf1\r\n0\t1\r\n5\t6\r\n10\t11\r\n15\t16\r\n20\t21"
    )


def test_cut_delimiter(cut_sample_csv: Path) -> None:
    """Test ``cut -d,``."""
    result = cut.cut_fields(file_path=cut_sample_csv, fields=[1], delimiter=",")
    expected = (
        'Song title\n"10000 Reasons (Bless the Lord)"'
        '\n"20 Good Reasons"\n"Adore You"\n"Africa"'
    )

    assert result == expected


def test_cut_delimiter_cli(
    capfd: pytest.CaptureFixture[str], cut_sample_csv: Path
) -> None:
    """Test ``cut -d,``."""
    exit_status = os.system(f"cccut -f1 -d, {cut_sample_csv}")
    captured = capfd.readouterr()
    assert exit_status == 0
    assert captured.out.rstrip() == (
        'Song title\r\n"10000 Reasons (Bless the Lord)"'
        '\r\n"20 Good Reasons"\r\n"Adore You"\r\n"Africa"'
    )
