from statfin.index_entry import IndexEntry
from statfin.variable import Value, Variable


_GAP = "  "
_MAX_LIST_ROWS = 8


def represent(name, *fields) -> str:
    s = ""
    s += f"{name}"
    for name, field in fields:
        s += _field(_GAP, name, field)
    return s


def _field(prefix, name, field) -> str:
    if field is None:
        return ""
    if isinstance(field, str):
        return f"\n{prefix}{name}: {field}"
    elif isinstance(field, list):
        return _list(prefix, name, field)
    else:
        raise AssertionError()


def _list(prefix, name, items) -> str:
    if len(items) == 0:
        return f"\n{prefix}{name}: (empty)"
    else:
        rows, widths = _itemrows(items)
        prefix2 = prefix + _GAP
        s = f"\n{prefix}{name}:"
        if len(items) <= _MAX_LIST_ROWS:
            for cols in rows:
                s += _item(prefix2, cols, widths)
        else:
            count = _MAX_LIST_ROWS - 1
            for cols in rows[:count]:
                s += _item(prefix2, cols, widths)
            s += f"\n{prefix2} ... and {len(items) - count} more"
        return s


def _itemrows(items) -> tuple[list[list[str]], list[int]]:
    rows = [_itemcols(item) for item in items]
    widths = [0] * len(rows[0])
    for cols in rows:
        for i, col in enumerate(cols):
            widths[i] = max(widths[i], len(col))
    return rows, widths


def _itemcols(item) -> list[str]:
    if isinstance(item, IndexEntry):
        typeid = f"({item.typeid})" if item.typeid else ""
        return [typeid, item.name, item.text]
    if isinstance(item, Value):
        return [item.code, item.text]
    if isinstance(item, Variable):
        return [f"[{len(item.values)}]", item.code, item.text]
    raise RuntimeError("Unrecognized item type", item)


def _item(prefix, cols: list[str], widths: list[int]) -> str:
    bits = [col.ljust(width) for col, width in zip(cols, widths)]
    return f"\n{prefix}{' '.join(bits)}"
