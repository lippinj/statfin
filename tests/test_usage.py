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

    df = table.query({
        "Alue": "SSS",                 # Single value
        "Pääasiallinen toiminta": "*", # All values
        "Sukupuoli": [1, 2],           # List of values
        "Ikä": "18-64",                # Single value
        "Vuosi": "2022",               # Single value
        "Tiedot": "vaesto",            # Single value
    })
    assert isinstance(df, pd.DataFrame)