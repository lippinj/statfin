from typing import Iterable

import dataclasses
import re


@dataclasses.dataclass
class Value:
    """Possible value of an independent variable"""

    code: str
    text: str

    def __repr__(self):
        """Representational string"""
        return f"Value({repr(self.code)}, {repr(self.text)})"


class Variable:
    """Independent variable in a table"""

    def __init__(self, j):
        self.code = j["code"]
        self.text = j["text"]
        self.values = [Value(c, t) for c, t in zip(j["values"], j["valueTexts"])]

    def __repr__(self) -> str:
        """Representational string"""
        from statfin.rendering import represent

        return represent(
            "statfin.Variable",
            ("code", self.code),
            ("text", self.text),
            ("values", self.values),
        )

    def __len__(self) -> int:
        """Number of values"""
        return len(self.values)

    def __iter__(self) -> Iterable[Value]:
        """Iterate values"""
        return iter(self.values)

    def __getattr__(self, code: str) -> Value:
        """Look up a value with the given code"""
        return self[code]

    def __getitem__(self, code: str) -> Value:
        """Look up a value with the given code"""
        for value in self.values:
            if value.code == code:
                return value
        raise IndexError(f"No value named {code} for the variable")

    @property
    def codes(self) -> list[str]:
        return [value.code for value in self.values]

    def find(self, pattern: str, flags: re.RegexFlag = re.IGNORECASE) -> list[Value]:
        """Find all values whose text matches the pattern"""
        prog = re.compile(pattern, flags)
        return [v for v in self.values if prog.search(v.text)]

    def to_query_set(self, query):
        """List of value codes for the given query spec"""
        if query == "*" or query is None:
            return self.codes
        elif isinstance(query, str):
            assert query in self.codes
            return [query]
        elif isinstance(query, Iterable):
            assert [q in self.codes for q in query]
            return list(query)
        else:
            assert str(query) in self.codes
            return [str(query)]
