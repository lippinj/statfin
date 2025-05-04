import pandas as pd

from statfin import cache
from statfin.requests import post
from statfin.variable import Variable


class Query:
    def __init__(self, table, cache_id: str | None = None):
        self._table = table
        self._cache_id = cache_id

    def __call__(self, **kwargs) -> pd.DataFrame:
        filters = self._parse_filters(**kwargs)
        if self._cache_id is None:
            return self._run(filters)
        else:
            return self._cached_run(filters)

    def _cached_run(self, filters) -> pd.DataFrame:
        assert self._cache_id is not None
        df = cache.load(self._cache_id, filters)
        if df is None:
            df = self._run(filters)
            cache.store(self._cache_id, df, filters)
        return df

    def _run(self, filters: dict) -> pd.DataFrame:
        return Result(self._fetch(filters)).df

    def _fetch(self, filters: dict):
        return post(self._table.url, json=Query._format_query(filters))

    def _parse_filters(self, **kwargs) -> dict:
        filters = {}
        for code, value in kwargs.items():
            variable = self._find_variable(code)
            filters[code] = variable.to_query_set(str(value))
        return filters

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


class Result:
    def __init__(self, j: dict):
        self.data = {}
        self.key_codes = []
        self.key_columns = []
        self.value_codes = []
        self.value_columns = []
        self._populate_columns(j["columns"])
        self._populate_data(j["data"])
        self.df = pd.DataFrame(data=self.data)

    def _populate_columns(self, j):
        for jc in j:
            code = jc["code"]
            typeid = jc["type"]
            self.data[code] = []
            if typeid == "c":
                self.value_codes.append(code)
                self.value_columns.append(self.data[code])
            else:
                self.key_codes.append(code)
                self.key_columns.append(self.data[code])

    def _populate_data(self, j):
        for jc in j:
            for col, value in zip(self.key_columns, jc["key"]):
                col.append(value)
            for col, value in zip(self.value_columns, jc["values"]):
                col.append(Result.parse_value(value))

    @staticmethod
    def parse_value(x: str):
        x = x.replace(" ", "").replace(",", ".")
        if x == "":
            return None
        if "." in x:
            return float(x)
        return int(x)
