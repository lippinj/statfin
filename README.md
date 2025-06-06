# Python interface for Finnish statistics databases

This package lets you talk to databases using the PxWeb API.

The PxWeb API is used by many Finnish statistics sources, notably those of
[Statistics Finland](https://stat.fi) (Tilastokeskus), the national statistical
institute.  For a list of available databases, take a look
[here](https://stat.fi/tup/tilastotietokannat/index_en.html#free-of-charge-databases).

![Usage example in Jupyter Notebook](./assets/jupyter_example_1.png)

## Installation

```bash
pip install statfin
```

## Quick start

```py
import statfin

# Create the API root object
db = statfin.StatFin()

# Navigate the content tree
print(db)                 # API root
print(db["StatFin"])      # Database named StatFin
print(db.StatFin.tyokay)  # Level named tyokay inside StatFin

# Locate the table of interest (the .px suffix can be omitted)
tbl = db.StatFin.tyokay["statfin_tyokay_pxt_115b.px"]
tbl = db.StatFin.tyokay.statfin_tyokay_pxt_115b

# In fact, any unambiguous part of the name suffices
tbl = db.StatFin.tyokay._115b

# Explore the table
print(tbl)             # Table information
print(tbl.Alue)        # Variable present in the table
print(tbl.Alue.KU941)  # Value that the variable can take

# Look up items in the variable values
tbl.Alue.find("vantaa")

# Query data from the table -- use codes found above
q = tbl.query()
q.Alue = "SSS"       # Single value
q.Vuosi = 2022       # Single value (cast to str)
q.Sukupuoli = [1, 2] # Specific values
q.Tiedot = "*"       # All values (this is the default)
response = q()
print(response.df)
```

## Usage

### Requirements

To install requirements with pip:

```sh
pip install -r requirements.txt
```

### Creating an interface

Create an instance of `statfin.PxWebAPI` with the URL of the API:

```py
>>> import statfin
>>> db = statfin.PxWebAPI(f"https://statfin.stat.fi/PXWeb/api/v1/fi")
```

For convenience, there are some predefined shortcuts to common databases:

```py
>>> db1 = statfin.StatFin()  # StatFin database
>>> db2 = statfin.Vero()     # Tax Administration database
>>> db3 = statfin.Vero("sv") # Same but in Swedish
```

The language is Finnish (`fi`) for default, but you can also specify English
(`en`) or Swedish (`sv`).

### Listing contents

The data provided by the API is laid out in a tree. The predefined interfaces
place you at the root, from where you can select one of a number of databases.
To list them, simply print the object:

```py
>>> db = statfin.StatFin()
>>> db
statfin.PxWebAPI
  url: https://statfin.stat.fi/PXWeb/api/v1/fi
  index:
     Check                               Check
     Hyvinvointialueet                   Hyvinvointialueet
     Kokeelliset_tilastot                Kokeelliset_tilastot
     Kuntien_avainluvut                  Kuntien_avainluvut
     Kuntien_talous_ja_toiminta          Kuntien_talous_ja_toiminta
     Maahanmuuttajat_ja_kotoutuminen     Maahanmuuttajat_ja_kotoutuminen
     Muuttaneiden_taustatiedot           Muuttaneiden_taustatiedot
     ... and 6 more
>>>
```

To descend to a child node from a particular location, use its name like an
index or like an attribute name, e.g. `db["StatFin"]` or `db.StatFin`.
Specifying just part of the name is enough, as long as it is ambiguous; for
example, `db.Posti` is enough to access `Postinumeroalueittainen_avoin_tieto`.

```py
>>> db.Posti
    statfin.PxWebAPI
      url: https://statfin.stat.fi/PXWeb/api/v1/fi/Postinumeroalueittainen_avoin_tieto
      title: Postinumeroalueittainen_avoin_tieto
      index:
        (l) uusin   Uusin aineisto
        (l) arkisto Arkisto
>>>
```

At the leaves of the tree, we find tables:

```py
>>> db.StatFin.tyokay._115b
statfin.Table
  url: https://statfin.stat.fi/PXWeb/api/v1/fi/StatFin/tyokay/statfin_tyokay_pxt_115b.px
  title: Väestö muuttujina Alue, Pääasiallinen toiminta, Sukupuoli, Ikä, Vuosi ja Tiedot
  variables:
    [310] Alue                   Alue
    [10]  Pääasiallinen toiminta Pääasiallinen toiminta
    [3]   Sukupuoli              Sukupuoli
    [4]   Ikä                    Ikä
    [37]  Vuosi                  Vuosi
    [1]   Tiedot                 Tiedot
>>>
```


### Using tables

The table has a number of variables, which you can access by indexing or
attribute-like access, like before:

```py
>>> tbl.Alue
statfin.Variable
  code: Alue
  text: Alue
  values:
    SSS   KOKO MAA
    KU020 Akaa
    KU005 Alajärvi
    KU009 Alavieska
    KU010 Alavus
    KU016 Asikkala
    KU018 Askola
     ... and 303 more
>>>
```

Use the `query()` method to construct a query object, the populate its
attributes to specify variable filters:

```py
>>> q = tbl.query()
>>> q.Vuosi = 2023
>>> q.Alue = "SSS"
>>> q["Pääasiallinen toiminta"] = "*"
```

For each variable, you can specify a single value, a list of values, or all
available values (by passing `"*"`). The default is to treat all variables as
`*`.

To execute the query and retrieve results, invoke the query object and read the
pandas DataFrame from the `df` field of the response object:

```py
>>> q().df
    Alue Pääasiallinen toiminta Sukupuoli    Ikä Vuosi   vaesto
0    SSS                    SSS       SSS    SSS  2023  5603851
1    SSS                    SSS       SSS   0-17  2023  1022205
2    SSS                    SSS       SSS  18-64  2023  3272270
3    SSS                    SSS       SSS    65-  2023  1309376
4    SSS                    SSS         1    SSS  2023  2773898
..   ...                    ...       ...    ...   ...      ...
115  SSS                     99         1    65-  2023     1697
116  SSS                     99         2    SSS  2023    93103
117  SSS                     99         2   0-17  2023     2402
118  SSS                     99         2  18-64  2023    88652
119  SSS                     99         2    65-  2023     2049

[120 rows x 6 columns]
>>>
```

To avoid fetching the same dataframes over and over, you can specify a caching
ID to the invocation:

```py
>>> q("my_cache_id")
```

This causes the results to be cached under the `.statfin_cache/` directory.
Queries with the same caching ID will return this table instead of re-fetching,
as long as the filter specs match.
