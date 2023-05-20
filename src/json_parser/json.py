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
        (TokenType.OPEN_BRACKET, re.compile(r"\[")),
        (TokenType.CLOSE_BRACKET, re.compile(r"\]")),
        (TokenType.OPEN_BRACE, re.compile(r"{")),
        (TokenType.CLOSE_BRACE, re.compile(r"}")),
        (
            TokenType.NUMBER,
            re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?"),
        ),
        (
            TokenType.STRING,
            re.compile(r"\"(?:[^\"\\\n\t]|\\[\"\\/bfnrt]|\\u[a-fA-F0-9]{4})*\""),
        ),
        (TokenType.NULL, re.compile(r"null")),
    ],
)


@dataclass(frozen=True)
class Token:
    """Holds information about string tokens."""

    pos: int
    type: TokenType
    value: str


class JSONLexerError(ValueError):
    """Raise when the string cannot be tokenized properly."""


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
        raise JSONLexerError(msg)

    @property
    def tokens(self) -> list[Token]:
        """Return the list of tokens."""
        return self._tokens


class JSONParser:
    """JSON Parser."""

    def __init__(self, tokens: list[Token], max_nesting: int = 19) -> None:
        self._tokens = tokens
        self._pos = 0
        self._nesting_level = 0
        self._nesting_max = max_nesting

    def current_type(self) -> TokenType:
        """Return the type of the token at the current pointer."""
        return self._tokens[self._pos].type

    @property
    def nesting_level(self) -> int:
        """Return the current nesting level."""
        return self._nesting_level

    @property
    def too_deep(self) -> bool:
        """Return whether the maximum nesting level was passed."""
        return self.nesting_level > self._nesting_max

    def next(self) -> None:
        """Advance the pointer."""
        self._pos += 1

    def depth_increase(self) -> None:
        """Increase nesting level."""
        self._nesting_level += 1

    def depth_decrease(self) -> None:
        """Decrease nesting level."""
        self._nesting_level -= 1

    def skip_whitespace(self) -> None:
        """Skip whitespace token."""
        if self.current_type() == TokenType.WHITESPACE:
            self.next()

    def validate(self) -> bool:
        """Return whether the list of tokens matches a valid JSON payload."""
        try:
            if self.current_type() == TokenType.OPEN_BRACE:
                if not self.validate_object():
                    return False
            elif self.current_type() == TokenType.OPEN_BRACKET:
                if not self.validate_array():
                    return False
            else:
                return False
            self.skip_whitespace()
            if self.current_type() != TokenType.EOF:
                return False
            return True
        except IndexError:
            return False

    def validate_object(self) -> bool:
        """Verify that the sequence of tokens is a ``object``."""
        self.depth_increase()
        if self.too_deep:
            return False
        self.next()  # Skip {
        self.skip_whitespace()
        while self.current_type() != TokenType.CLOSE_BRACE:
            if self.current_type() != TokenType.STRING:
                return False
            self.next()
            self.skip_whitespace()
            if self.current_type() != TokenType.COLON:
                return False
            self.next()
            if not self.validate_value():
                return False
            # Skip ,
            if self.current_type() == TokenType.COMMA:
                self.next()
                self.skip_whitespace()
                # , cannot be followed by }
                if self.current_type() == TokenType.CLOSE_BRACE:
                    return False
        self.next()  # Skip }
        self.depth_decrease()
        return True

    def validate_array(self) -> bool:
        """Verify that the sequence of tokens is a ``array``."""
        self.depth_increase()
        if self.too_deep:
            return False
        self.next()  # Skip [
        self.skip_whitespace()
        while self.current_type() != TokenType.CLOSE_BRACKET:
            if not self.validate_value():
                return False
            # self.next()
            # Skip ,
            if self.current_type() == TokenType.COMMA:
                self.next()
                # , cannot be followed by ]
                if self.current_type() == TokenType.CLOSE_BRACKET:
                    return False
        self.next()  # Skip ]
        self.depth_decrease()
        return True

    def validate_value(self) -> bool:
        """Verify that the sequence of tokens is a ``value``."""
        self.skip_whitespace()
        # Test for valid values
        if self.current_type() in {
            TokenType.NULL,
            TokenType.FALSE,
            TokenType.TRUE,
            TokenType.NUMBER,
            TokenType.STRING,
        }:
            self.next()
        elif (
            self.current_type() == TokenType.OPEN_BRACKET and self.validate_array()
        ) or (self.current_type() == TokenType.OPEN_BRACE and self.validate_object()):
            # {} and [] will advance past the right delimiter upon validation
            pass
        else:
            return False
        self.skip_whitespace()
        return True
