# Python interface for Finnish statistics databases

This package lets you talk to databases using the PxWeb API.

The PxWeb API is used by many Finnish statistics sources, notably those of
[Statistics Finland](https://stat.fi) (Tilastokeskus), the national statistical institute.

Results are usually given directly as pandas dataframes.

## Quick start

```py
import statfinpy

# Create top level database API interface
db = statfinpy.Database.StatFin()
#db = Database.StatFin("en") # In English
#db = Database.Vero()        # Database API for Verohallinto

# Explore the contents of the database API:
print(db.ls())                    # List databases
print(db.ls("StatFin"))           # List database levels
print(db.ls("StatFin", "tyokay")) # List database tables

# Create an interface to a table
tbl = db.table("StatFin", "statfin_tyokay_pxt_115b.px")

# Explore the metadata of the table:
print(tbl.title)           # Human readable title
print(tbl.variables)       # Queryable variables
print(tbl.values["Alue"])  # Possible values for a variable

# Query data from the table -- refer to table.values for codes
df = tbl.query({
    "Alue": "SSS",                 # Single value
    "Pääasiallinen toiminta": "*", # All values
    "Sukupuoli": [1, 2],           # List of values
    "Ikä": "18-64",                # Single value
    "Vuosi": "2022",               # Single value
    "Tiedot": "vaesto",            # Single value
})
print(df)
```