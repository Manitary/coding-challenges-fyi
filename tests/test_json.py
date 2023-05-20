"""Test for JSON parser."""

from conftest import JSONTestFile
import json_parser


def test_json_parser(sample_json: JSONTestFile) -> None:
    """Test the JSON files."""
    # result = json_parser.parse(sample_json.path)
    result = json_parser.parse(sample_json)
    assert sample_json.result == result
