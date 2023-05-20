"""Test for JSON parser."""

from conftest import JSONTestFile
import json_parser


def test_json_parser(sample_json: JSONTestFile) -> None:
    """Test the JSON files."""
    # result = json_parser.parse(sample_json.path)
    with open(sample_json.path, encoding="utf8") as f:
        lexer = json_parser.Lexer(f.read())
    try:
        lexer.tokenize()
        for token in lexer.tokens:
            print(f"{token.type} | {token.value}")
        parser = json_parser.JSONParser(lexer.tokens)
        result = parser.validate()
        assert sample_json.result == result
    except json_parser.JSONLexerError:
        assert sample_json.result is False
