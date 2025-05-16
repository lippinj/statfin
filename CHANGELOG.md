## 0.3.0

- Automatically parse time colums as a datetime type

## 0.2.1

- Fixed some number parsing

## 0.2.0

- Change the interface to use `__getitem__` and `__getattr__` for locating levels, tables etc. For example: instead of `db.table("StatFin", "ati", "statfin_ati_pxt_11zt.px")`, write `db["StatFin"]["ati"]["statfin_ati_pxt_11zt"]` or `db.Statfin.ati.statfin_ati_pxt_11zt`
- Add functionality to look up items in tables of code/text pairs more easily
- Allow partial name lookup
- Improve query syntax
- Add custom `repr` strings for many types

## 0.1.1

- Add an exception type for bad requests

## 0.1.0

- Fix decimal numbers being parsed as `None`
