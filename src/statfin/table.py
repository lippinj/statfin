from typing import Iterable

import pandas as pd

import statfin
from statfin.variable import Variable
from statfin.requests import get, post


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
        s = "statfin.Table\n"
        s += f"  url: {self.url}\n"
        if self.title:
            s += f"  title: {self.title}\n"
        if len(self.variables) == 0:
            s += "  variables: (none)\n"
        else:
            s += "  variables:\n"
            width = max([len(variable.code) for variable in self.variables])
            for variable in self.variables:
                s += f"    {variable.code.ljust(width)} {variable.text}\n"
        return s

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

    def query(self, filters, cache: str | None = None) -> pd.DataFrame:
        """Query data from the API

        Pass filters in as keyword arguments, like code=value. The value
        may be a single value, a list of values, or "*" to indicate all
        values.

        Returns a DataFrame.
        """
        if cache is None:
            filters = self._expand_filters(filters)
            return _parse_result(self.query_raw(filters))
        else:
            df = statfin.cache.load(cache, filters)
            if df is not None:
                return df
            else:
                df = self.query(filters)
                statfin.cache.store(cache, df, filters)
                return df

    def query_raw(self, filters):
        """Query data from the API (raw JSON)"""
        return post(self.url, json=_format_payload(filters))

    def _expand_filters(self, filters):
        out = {}
        for code, values in filters.items():
            if values == "*":
                values = [value.code for value in self[code]]
            if not isinstance(values, (list, tuple)):
                values = [values]
            out[code] = values
        return out


def _format_payload(filters, response_format="json"):
    return {
        "response": {"format": response_format},
        "query": _format_query(filters),
    }


def _format_query(filters):
    query = []
    for code, values in filters.items():
        selection = _format_selection(values)
        query.append({"code": code, "selection": selection})
    return query


def _format_selection(value):
    return {
        "filter": "item",
        "values": value,
    }


def _parse_result(j):
    kcol, vcol = _parse_result_columns(j["columns"])
    data = _parse_result_data(j["data"], kcol, vcol)
    return pd.DataFrame(data=data)


def _parse_result_columns(j):
    key_cols = []
    value_cols = []
    for j_col in j:
        code = j_col["code"]
        typ = j_col["type"]
        if typ == "c":
            value_cols.append(code)
        else:
            key_cols.append(code)
    return key_cols, value_cols


def _parse_result_data(j, key_cols, value_cols):
    all_cols = key_cols + value_cols
    data = {code: [] for code in all_cols}
    key = [data[code] for code in key_cols]
    val = [data[code] for code in value_cols]
    for j_data in j:
        for col, v in zip(key, j_data["key"]):
            col.append(v)
        for col, v in zip(val, j_data["values"]):
            col.append(_to_value(v))
    return data


def _to_value(x):
    x = x.replace(" ", "").replace(",", ".")
    try:
        return int(x)
    except ValueError:
        pass
    try:
        return float(x)
    except ValueError:
        pass
    return None
