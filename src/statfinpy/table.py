import pandas as pd
import requests


class Table:
    """Interface to a PxWeb table"""

    def __init__(self, url: str):
        """
        Interface to a table with the given endpoint URL

        Users normally want to create a table by calling
        Database.table() rather than directly.
        """
        self._url = url
        self._title = None
        self._variables = None
        self._values = None

    @property
    def title(self):
        """Human readable title for this table

        Lazily loads the table metadata, if not already loaded.
        """
        if self._title is None:
            self._fetch_metadata()
        return self._title

    @property
    def variables(self):
        """Queryable variables

        This is a DataFrame containing variable codes and human readable
        descriptions.

        Lazily loads the table metadata, if not already loaded.
        """
        if self._variables is None:
            self._fetch_metadata()
        return self._variables

    @property
    def values(self):
        """Values of the queryable variables

        This is a dictionary from variable code to a DataFrame
        containing value codes and human readable descriptions.

        Lazily loads the table metadata, if not already loaded.
        """
        if self._values is None:
            self._fetch_metadata()
        return self._values

    def query(self, filters):
        """Query data from the API

        Pass filters in as keyword arguments, like code=value. The value
        may be a single value, a list of values, or "*" to indicate all
        values.

        Returns a DataFrame.
        """
        filters = self._expand_filters(filters)
        return _parse_result(self.query_raw(filters))

    def query_raw(self, filters):
        """Query data from the API (raw JSON)"""
        return self._post(_format_payload(filters))

    def _post(self, payload):
        r = requests.post(self._url, json=payload)
        return r.json()

    def _fetch_metadata(self):
        j = requests.get(self._url).json()
        self._title = j["title"]
        self._variables = pd.DataFrame(
            data={
                "code": [jv["code"] for jv in j["variables"]],
                "text": [jv["text"] for jv in j["variables"]],
            }
        )
        self._values = {
            jv["code"]: pd.DataFrame(
                data={
                    "code": jv["values"],
                    "text": jv["valueTexts"],
                }
            )
            for jv in j["variables"]
        }

    def _expand_filters(self, filters):
        out = {}
        for code, values in filters.items():
            if values == "*":
                values = list(self.values[code].code)
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
    try:
        xf = float(x)
        xi = int(x)
        return xf if xf == xi else xi
    except ValueError:
        return None
