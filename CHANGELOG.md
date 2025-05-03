## 0.2.0

- Change the interface to use `__getitem__` and `__getattr__` for locating levels, tables etc. For example: instead of `db.table("StatFin", "ati", "statfin_ati_pxt_11zt.px")`, write `db["StatFin"]["ati"]["statfin_ati_pxt_11zt"]` or `db.Statfin.ati.statfin_ati_pxt_11zt`
- Add functionality to look up items in tables of code/text pairs more easily
- Allow partial name lookup
- Add custom `repr` strings for many types

## 0.1.1

- Add an exception type for bad requests

## 0.1.0

- Fix decimal numbers being parsed as `None`
