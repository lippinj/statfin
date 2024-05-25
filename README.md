# Python API for Tilastokeskus (Statistics Finland)

This package talks to the PxWeb API through which
[Tilastokeskus](https://stat.fi/) (Statistics Finland in English)
provides convenient access to its databases as pandas DataFrames.
Verohallinto also exposes its databases in this way.

To find interesting databases, you can explore the web UI:
[StatFin](https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/),
[Vero](https://vero2.stat.fi/PXWeb/pxweb/fi/Vero/).

## Quick start

```py
from statfinpy import DatabaseApi

# Create top level database API interface
api = DatabaseApi.StatFin()
#api = DatabaseApi.StatFin("en") # In English
#api = DatabaseApi.Vero()        # Database API for Verohallinto

# Explore the contents of the database API:
print(api.ls())                    # List databases
print(api.ls("StatFin"))           # List database levels
print(api.ls("StatFin", "tyokay")) # List database tables

# Create an interface to a table
table = api.table("StatFin", "statfin_tyokay_pxt_115b.px")

# Explore the metadata of the table:
print(table.title)           # Human readable title
print(table.variables)       # Queryable variables
print(table.values["Alue"])  # Possible values for a variable

# Query data from the table -- refer to table.values for codes
df = table.query({
    "Alue": "SSS",                 # Single value
    "Pääasiallinen toiminta": "*", # All values
    "Sukupuoli": [1, 2],           # List of values
    "Ikä": "18-64",                # Single value
    "Vuosi": "2022",               # Single value
    "Tiedot": "vaesto",            # Single value
})
```