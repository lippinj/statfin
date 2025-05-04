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

    q = tbl.query(Alue="SSS", Tiedot="vaesto")
    q["Pääasiallinen toiminta"] = "*"  # All values
    q.Vuosi = 2023  # Single value (will be cas to str)
    q.Sukupuoli = [1, 2]  # Multiple values
    q.Ikä = "18-64"  # Single value
    df = q()

    assert isinstance(df, pd.DataFrame)


def test_cached_query():
    statfin.cache.clear()
    db = statfin.StatFin()
    tbl = db.StatFin.tyokay._115b

    q = tbl.query(Alue="SSS", Tiedot="vaesto")
    df = q("test")  # With cache id "test"

    assert isinstance(df, pd.DataFrame)
    assert os.path.isfile(".statfin_cache/test.df")
    assert os.path.isfile(".statfin_cache/test.meta")

    df = q("test")
    assert isinstance(df, pd.DataFrame)


def test_handles_comma_separator():
    db = statfin.StatFin()
    tbl = db.StatFin.ntp._11tj

    df = tbl.query(Taloustoimi="E2", Toimiala="SSS")()

    assert df.KAUSIT.notna().all()
    assert df.TASM.notna().all()
    assert df.TRENDI.notna().all()
    assert df.TYOP.notna().all()
