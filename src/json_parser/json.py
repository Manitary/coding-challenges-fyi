"""A JSON parser."""

import re
from enum import IntEnum, auto
from dataclasses import dataclass


class TokenType(IntEnum):
    """Tokens found when lexing a string."""

    STRING = auto()
    NUMBER = auto()
    OPEN_BRACE = auto()
    CLOSE_BRACE = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()
    COMMA = auto()
    WHITESPACE = auto()
    COLON = auto()
    NULL = auto()
    TRUE = auto()
    FALSE = auto()
    EOF = auto()


TOKEN_DEFINITION: list[tuple[TokenType, re.Pattern[str]]] = sorted(
    [
        (TokenType.EOF, re.compile(r"$")),
        (TokenType.TRUE, re.compile(r"true")),
        (TokenType.FALSE, re.compile(r"false")),
        (TokenType.WHITESPACE, re.compile(r"\s+")),
        (TokenType.COLON, re.compile(r":")),
        (TokenType.COMMA, re.compile(r",")),
        (TokenType.CLOSE_BRACKET, re.compile(r"\]")),
        (TokenType.OPEN_BRACKET, re.compile(r"\[")),
        (TokenType.OPEN_BRACE, re.compile(r"{")),
        (TokenType.CLOSE_BRACE, re.compile(r"}")),
        (TokenType.NUMBER, re.compile(r"\d+")),
    ],
)


@dataclass(frozen=True)
class Token:
    """Holds information about string tokens."""

    pos: int
    type: TokenType
    value: str


class Lexer:
    """Tokenize a string."""

    def __init__(self, text: str) -> None:
        self._text = text
        self._pos = 0
        self._tokens: list[Token] = []

    def tokenize(self) -> None:
        """Tokenize the currently held string.

        Store the resulting tokens in self._tokens."""
        while True:
            token = self.get_next_token()
            self._tokens.append(token)
            if token.type == TokenType.EOF:
                break

    def get_next_token(self) -> Token:
        """Return the next token from the current position."""
        for token_type, pattern in TOKEN_DEFINITION:
            if match := pattern.match(self._text, pos=self._pos):
                value = match.group()
                self._pos += len(value)
                return Token(self._pos, token_type, value)

        chunk = self._text[self._pos : self._pos + 20]
        msg = f"Unrecognized token: position={self._pos} content={chunk!r}"
        raise ValueError(msg)


class JSONParser:
    """JSON Parser."""
    