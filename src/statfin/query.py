import pandas as pd

from statfin import cache
from statfin.query_response import QueryResponse
from statfin.requests import post
from statfin.table_response import TableResponse
from statfin.variable import Variable


class Query:
    def __init__(self, table):
        self._table = table
        self._filters = {}
        for variable in self._table.variables:
            self[variable.code] = variable.codes

    def __setattr__(self, name, value):
        """Set the filter for the given code"""
        if name in ("_table", "_filters"):
            object.__setattr__(self, name, value)
        else:
            self[name] = value

    def __setitem__(self, code, spec):
        """Set the filter for the given code"""
        variable = self._find_variable(code)
        self._filters[code] = variable.to_query_set(spec)

    def __call__(self, cache_id: str | None = None) -> QueryResponse:
        if cache_id is None:
            return QueryResponse(self._fetch())
        else:
            return QueryResponse(self._cached_fetch(cache_id))

    def _fetch(self) -> pd.DataFrame:
        return TableResponse(self._fetch_json()).df

    def _cached_fetch(self, cache_id: str) -> pd.DataFrame:
        df = cache.load(cache_id, self._filters)
        if df is None:
            df = self._fetch()
            cache.store(cache_id, df, self._filters)
        return df

    def _fetch_json(self) -> dict:
        return post(self._table.url, json=Query._format_query(self._filters))

    def _find_variable(self, name) -> Variable:
        candidates = self._find_variable_candidates(name)
        if len(candidates) == 1:
            return candidates[0]
        elif len(candidates) == 0:
            raise IndexError(f"Variable not found: {name}")
        else:
            raise IndexError(f"Variable is ambiguous: {name}")

    def _find_variable_candidates(self, name) -> list[Variable]:
        candidates = []
        for variable in self._table.variables:
            if variable.code == name:
                return [variable]
            if name in variable.code:
                candidates.append(variable)
        return candidates

    @staticmethod
    def _format_query(filters: dict) -> dict:
        return {
            "response": {"format": "json"},
            "query": [
                {"code": code, "selection": {"filter": "item", "values": values}}
                for code, values in filters.items()
            ],
        }
