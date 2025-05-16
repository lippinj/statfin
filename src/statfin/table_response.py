from dataclasses import dataclass
from datetime import datetime
import re

import numpy as np
import pandas as pd


class TableResponse:
    """Parsed response to a table retrieval query"""

    def __init__(self, j: dict):
        self.columns: Columns = Columns.from_json(j["columns"])
        self.raw: dict = parse_raw(j["data"], self.columns)
        self.df: pd.DataFrame = build_dataframe(self.raw, self.columns)


@dataclass
class Dimension:
    code: str
    text: str
    time: bool = False


@dataclass
class Measure:
    code: str
    text: str
    unit: str | None = None


class Columns:
    def __init__(self):
        self.dimensions: list[Dimension] = []
        self.measures: list[Measure] = []

    @property
    def all(self) -> list[Dimension | Measure]:
        return [*self.dimensions, *self.measures]

    def __getitem__(self, code: str) -> Dimension | Measure:
        for col in self.all:
            if col.code == code:
                return col
        raise ValueError(f"No column with code {code}")

    @staticmethod
    def from_json(j: list[dict]):
        columns = Columns()
        for jc in j:
            code = jc["code"]
            text = jc["text"]
            typeid = jc.get("type", "d")
            assert typeid in ("d", "t", "c")
            if typeid in ("d", "t"):
                time = typeid == "t"
                columns.dimensions.append(Dimension(code, text, time))
            else:
                unit = jc.get("unit", None)
                columns.measures.append(Measure(code, text, unit))
        return columns


def parse_raw(j: list[dict], cols: Columns) -> dict:
    raw = {col.code: [] for col in cols.all}
    for jr in j:
        for s, col in zip([*jr["key"], *jr["values"]], cols.all):
            raw[col.code].append(s)
    return raw


def build_dataframe(raw: dict, cols: Columns) -> pd.DataFrame:
    data = {code: interpret(cols[code], vals) for code, vals in raw.items()}
    return pd.DataFrame(data)


def interpret(col: Dimension | Measure, values: list) -> list:
    if isinstance(col, Measure):
        return [parse_number(x) for x in values]
    elif col.time:
        return [parse_time(x) for x in values]
    else:
        return values


def parse_number(x) -> float:
    try:
        if isinstance(x, str):
            x = x.strip()
            x = x.replace(",", ".")  # Undo comma decimal separator
            x = x.replace(" ", "")  # Undo extra spaces
        return float(x)
    except ValueError:
        return float(np.nan)


def parse_time(x: str) -> datetime | str:
    x = x.strip()
    if re.fullmatch(r"\d{4}", x):
        return datetime.strptime(x, "%Y")
    elif re.fullmatch(r"\d{4}M\d{2}", x):
        return datetime.strptime(x, "%YM%m")
    else:
        return x
