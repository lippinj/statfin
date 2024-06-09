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

db = statfin.PxWebAPI.StatFin()

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
>>> db1 = statfin.PxWebAPI.StatFin()          # StatFin database
>>> db2 = statfin.PxWebAPI.Verohallinto()     # Tax Administration database
>>> db3 = statfin.PxWebAPI.Verohallinto("sv") # Same but in Swedish
```

The language is Finnish (`fi`) for default, but you can also specify English
(`en`) or Swedish (`sv`).

### Listing contents

Use the `ls()` method to list available contents at various depths. The listing
is returned as a dataframe. To list databases:

```py
>>> db.ls()
                                   dbid                                 text
0                                 Check                                Check
1                              Explorer                             Explorer
2                     Hyvinvointialueet                    Hyvinvointialueet
3                  Kokeelliset_tilastot                 Kokeelliset_tilastot
4                    Kuntien_avainluvut                   Kuntien_avainluvut
5            Kuntien_talous_ja_toiminta           Kuntien_talous_ja_toiminta
6       Maahanmuuttajat_ja_kotoutuminen      Maahanmuuttajat_ja_kotoutuminen
7             Muuttaneiden_taustatiedot            Muuttaneiden_taustatiedot
8   Postinumeroalueittainen_avoin_tieto  Postinumeroalueittainen_avoin_tieto
9                                   SDG                                  SDG
10                              StatFin                              StatFin
11                     StatFin_Passiivi                     StatFin_Passiivi
12                   Toimipaikkalaskuri                   Toimipaikkalaskuri
```

To list layers within a database:

```py
>>> db.ls("StatFin")
        id type                                      text
0    adopt    l                                  Adoptiot
1      aku    l         Aikuiskoulutukseen osallistuminen
2      ava    l                              Ainevalinnat
3     akay    l                                Ajankäyttö
4      aly    l      Aloittaneet ja lopettaneet yritykset
..     ...  ...                                       ...
141  ympsm    l                    Ympäristönsuojelumenot
142   ymtu    l                             Ympäristötuet
143    yev    l                            Ympäristöverot
144   yrti    l  Yritysten rakenne- ja tilinpäätöstilasto
145   yrtt    l                         Yritystukitilasto

[146 rows x 3 columns]
```

To list tables belonging to a layer:

```py
>>> db.ls("StatFin", "akay")
                         id type                                               text              updated
0   statfin_akay_pxt_001.px    t                 001 -- Ajankäyttö (26 lk) syksyllä  2019-09-13T14:43:44
1   statfin_akay_pxt_002.px    t  002 -- Ajankäyttö (26 lk) pääasiallisen toimin...  2017-10-09T10:40:08
2   statfin_akay_pxt_003.px    t  003 -- Työllisten miesten ja naisten ajankäytt...  2017-10-09T10:40:08
3   statfin_akay_pxt_004.px    t       004 -- Ajankäyttö (26 lk) elinvaiheen mukaan  2017-10-09T10:40:08
4   statfin_akay_pxt_005.px    t        005 -- Ajankäyttö (82 lk) sukupuolen mukaan  2017-10-09T10:40:08
5   statfin_akay_pxt_006.px    t               006 -- Ajankäyttö (82 lk) iän mukaan  2019-09-19T08:44:44
6   statfin_akay_pxt_007.px    t  007 -- Yli 10-vuotiaiden ajankäyttö (132 lk) s...  2017-10-09T10:40:08
7   statfin_akay_pxt_008.px    t  008 -- Kirjastossa käyminen 12 kuukauden aikan...  2017-10-09T10:40:08
8   statfin_akay_pxt_009.px    t  009 -- Kirjastossa käyminen 12 kuukauden aikan...  2017-10-09T10:40:08
9   statfin_akay_pxt_010.px    t  010 -- Kirjastossa käyminen 12 kuukauden aikan...  2017-10-09T10:40:08
10  statfin_akay_pxt_011.px    t  011 -- Lukemiseen käytetty aika sukupuolen ja ...  2019-09-19T08:44:44
11  statfin_akay_pxt_012.px    t            012 -- Kulttuuritilaisuuksissa käyminen  2019-09-19T08:44:44
12  statfin_akay_pxt_013.px    t             013 -- Luovien taiteiden harrastaminen  2019-09-19T08:44:44
```

### Creating a table interface

To access a specific table, call the method `table(database, layer, table_name)`:

```py
>>> table = db.table("StatFin", "akay", "statfin_akay_pxt_006.px")
```

For newer API versions, the layer can be omitted:

```py
>>> table = db.table("StatFin", "statfin_akay_pxt_006.px")
```

### Reading table metadata

Table title:

```py
>>> table.title
'006 -- Ajankäyttö (82 lk) iän mukaan'
```

Table variables (as a dataframe):

```py
>>> table.variables
        code       text
0   Toiminto   Toiminto
1        Ikä        Ikä
2  Sukupuoli  Sukupuoli
3     Vuodet     Vuodet
```

Table variables (as a dataframe):

```py
>>> table.variables
        code       text
0   Toiminto   Toiminto
1        Ikä        Ikä
2  Sukupuoli  Sukupuoli
3     Vuodet     Vuodet
```

Possible values for the variables (as a mapping of variable code to dataframe):

```py
>>> table.values.keys()
dict_keys(['Toiminto', 'Ikä', 'Sukupuoli', 'Vuodet'])
>>> table.values["Vuodet"]
        code       text
0  1987-1988  1987-1988
1  1999-2000  1999-2000
2  2009-2010  2009-2010
```

### Querying table contents

Use the `query()` method to query data filtered by variables as a dataframe.

For each variable, you can specify a single value, a list of values or all
values (`*`). Make sure to use variable codes, not human readable names!

```py
>>> table.query({
...         "Toiminto": "*",
...         "Ikä": [1, 2, 3],
...         "Sukupuoli": "S",
...         "Vuodet": "2009-2010"
...     })
    Toiminto Ikä Sukupuoli     Vuodet Ajankäyttö (82 lk)
0      01-82   1         S  2009-2010               None
1      01-82   2         S  2009-2010               None
2      01-82   3         S  2009-2010               None
3      01-03   1         S  2009-2010               None
4      01-03   2         S  2009-2010               None
..       ...  ..       ...        ...                ...
292       81   2         S  2009-2010               None
293       81   3         S  2009-2010               None
294       82   1         S  2009-2010               None
295       82   2         S  2009-2010               None
296       82   3         S  2009-2010               None

[297 rows x 5 columns]
```