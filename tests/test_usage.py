import os
import pandas as pd
import statfin


def test_Verohallinto():
    db = statfin.PxWebAPI.Verohallinto()
    assert isinstance(db.ls(), pd.DataFrame)
    assert isinstance(db.ls("Vero"), pd.DataFrame)


def test_StatFin():
    db = statfin.PxWebAPI.StatFin()
    assert isinstance(db.ls(), pd.DataFrame)
    assert isinstance(db.ls("StatFin"), pd.DataFrame)
    assert isinstance(db.ls("StatFin", "tyokay"), pd.DataFrame)

    table = db.table("StatFin", "statfin_tyokay_pxt_115b.px")
    assert isinstance(table.title, str)
    assert isinstance(table.variables, pd.DataFrame)
    assert isinstance(table.values["Alue"], pd.DataFrame)

    df = table.query(
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

    db = statfin.PxWebAPI.StatFin()
    table = db.table("StatFin", "statfin_tyokay_pxt_115b.px")

    df = table.query(
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

    df = table.query(
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
    db = statfin.PxWebAPI.StatFin()
    table = db.table("StatFin", "statfin_ntp_pxt_11tj.px")
    df = table.query({
        "Vuosineljännes": "*",
        "Taloustoimi": "E2",
        "Toimiala": "SSS",
    })
    assert(df.KAUSIT.notna().all())
    assert(df.TASM.notna().all())
    assert(df.TRENDI.notna().all())
    assert(df.TYOP.notna().all())
