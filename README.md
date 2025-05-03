# Python interface for Finnish statistics databases

This package lets you talk to databases using the PxWeb API.

The PxWeb API is used by many Finnish statistics sources, notably those of
[Statistics Finland](https://stat.fi) (Tilastokeskus), the national statistical
institute.  For a list of available databases, take a look
[here](https://stat.fi/tup/tilastotietokannat/index_en.html#free-of-charge-databases).

Results of queries and listings are returned as pandas DataFrames.

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
  contents:
      Check                               Check
      Hyvinvointialueet                   Hyvinvointialueet
      Kokeelliset_tilastot                Kokeelliset_tilastot
      Kuntien_avainluvut                  Kuntien_avainluvut
      Kuntien_talous_ja_toiminta          Kuntien_talous_ja_toiminta
      Maahanmuuttajat_ja_kotoutuminen     Maahanmuuttajat_ja_kotoutuminen
      Muuttaneiden_taustatiedot           Muuttaneiden_taustatiedot
      Postinumeroalueittainen_avoin_tieto Postinumeroalueittainen_avoin_tieto
      SDG                                 SDG
      StatFin                             StatFin
      StatFin_Passiivi                    StatFin_Passiivi
      Toimipaikkalaskuri                  Toimipaikkalaskuri
      ymp                                 ymp
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
  contents:
    l uusin   Uusin aineisto
    l arkisto Arkisto
```

At the leaves of the tree, we find tables:

```py
>>> db.StatFin.vaerak._14x5
statfin.Table
  url: https://statfin.stat.fi/PXWeb/api/v1/fi/StatFin/vaerak/statfin_vaerak_pxt_14x5.px
  title: Väestö 31.12. muuttujina Vuosi, Taajama ja Tiedot
  variables:
    Vuosi   Vuosi
    Taajama Taajama
    Tiedot  Tiedot
```

### Using tables

The table has a number of variables, which you can access by indexing or
attribute-like access, like before:

```py
>>> tbl.Taajama
statfin.Variable
  code: Taajama
  text: Taajama
  values:
    TA2320 Ahde
    TA0146 Ahlainen
    TA1109 Ahola (Posio)
    TA1163 Ahonkylä
    ...
```

Use the `query()` method to query data filtered by variables as a dataframe.

For each variable, you can specify a single value, a list of values or all
values (`*`). Make sure to use variable codes, not human readable names!
