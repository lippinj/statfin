import os
import pandas as pd
import pytest
import statfin


def test_Vero():
    db = statfin.Vero()
    assert db.url == "https://vero2.stat.fi/PXWeb/api/v1/fi"


def test_StatFin():
    db = statfin.StatFin()
    assert db.url == "https://statfin.stat.fi/PXWeb/api/v1/fi"

def test_drilling():
    db = statfin.Vero()
    assert isinstance(db.Vero, statfin.PxWebAPI)
    assert isinstance(db.Vero.Henk, statfin.PxWebAPI)
    assert isinstance(db.Vero.Henk.lopulliset, statfin.PxWebAPI)
    assert isinstance(db.Vero.Henk.lopulliset.tulot._101, statfin.Table)
    assert isinstance(db["Vero"]["Henk"].lopulliset["tulot"]._101, statfin.Table)
    
def test_variables():
    db = statfin.StatFin()
    tbl = db.StatFin.tyokay._115b
    assert isinstance(tbl.Alue, statfin.Variable)
    assert isinstance(tbl["Alue"], statfin.Variable)
    assert isinstance(tbl.Alue.SSS, statfin.Value)
    assert isinstance(tbl.Alue["SSS"], statfin.Value)

def test_query():
    db = statfin.StatFin()
    tbl = db.StatFin.tyokay._115b
    df = tbl.query(
        {
            "Alue": "SSS",  # Single value
            "Pääasiallinen toiminta": "*",  # All values
            "Sukupuoli": [1, 2],  # List of values
            "Ikä": "18-64",  # Single value
            "Vuosi": "2022",  # Single value
            "Tiedot": "vaesto",  # Single value
        }
    )
    assert isinstance(df, pd.DataFrame)


def test_cached_query():
    statfin.cache.clear()
    db = statfin.StatFin()
    tbl = db.StatFin.tyokay._115b
    df = tbl.query(
        {
            "Alue": "SSS",
            "Pääasiallinen toiminta": "*",
            "Sukupuoli": [1, 2],
            "Ikä": "18-64",
            "Vuosi": "2022",
            "Tiedot": "vaesto",
        },
        cache="test",
    )
    assert isinstance(df, pd.DataFrame)
    assert os.path.isfile(".statfin_cache/test.df")
    assert os.path.isfile(".statfin_cache/test.meta")

    df = tbl.query(
        {
            "Alue": "SSS",
            "Pääasiallinen toiminta": "*",
            "Sukupuoli": [1, 2],
            "Ikä": "18-64",
            "Vuosi": "2022",
            "Tiedot": "vaesto",
        },
        cache="__test.cached.df",
    )
    assert isinstance(df, pd.DataFrame)


def test_handles_comma_separator():
    db = statfin.StatFin()
    tbl = db.StatFin.ntp._11tj
    df = tbl.query({
        "Vuosineljännes": "*",
        "Taloustoimi": "E2",
        "Toimiala": "SSS",
    })
    assert(df.KAUSIT.notna().all())
    assert(df.TASM.notna().all())
    assert(df.TRENDI.notna().all())
    assert(df.TYOP.notna().all())

