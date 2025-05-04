from typing import Iterable

from statfin.query import Query
from statfin.requests import get
from statfin.variable import Variable


class Table:
    """Interface to a PxWeb table"""

    def __init__(self, url: str, j: dict | None = None):
        """
        Interface to a table with the given endpoint URL

        Users normally want to create a table by calling
        Database.table() rather than directly.
        """
        j = j or get(url)
        self.url = url
        self.title = j["title"]
        self.variables = [Variable(jv) for jv in j["variables"]]

    def __repr__(self):
        """Representational string"""
        from statfin.rendering import represent

        return represent(
            "statfin.Table",
            ("url", self.url),
            ("title", self.title),
            ("variables", self.variables),
        )

    def __iter__(self) -> Iterable[Variable]:
        """Iterate variables"""
        return iter(self.variables)

    def __getattr__(self, code: str) -> Variable:
        """Look up a variable with the given code"""
        return self[code]

    def __getitem__(self, code: str) -> Variable:
        """Look up a variable with the given code"""
        for variable in self.variables:
            if variable.code == code:
                return variable
        raise IndexError(f"No variable named {code} in the table")

    def query(self, **kwargs) -> Query:
        """Query data from the API"""
        query = Query(self)
        for code, spec in kwargs.items():
            query[code] = spec
        return query
