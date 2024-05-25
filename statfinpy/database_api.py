import pandas as pd
import requests

from statfinpy.table import Table


class DatabaseApi:
    """PxWeb API (contains some number of databases)"""

    @staticmethod
    def StatFin(lang: str = "fi"):
        """Statistics API for Tilastokeskus (Statistics Finland)

        Optionally, you can specify the language (fi/en/sv).
        """
        url = f"https://statfin.stat.fi/PXWeb/api/v1/{lang}"
        return DatabaseApi(url)

    @staticmethod
    def Vero(lang: str = "fi"):
        """Statistics API for Verohallinto

        Optionally, you can specify the language (fi/en/sv).
        """
        url = f"https://vero2.stat.fi/PXWeb/api/v1/{lang}"
        return DatabaseApi(url)

    def __init__(self, url: str):
        """API located at the given URL"""
        self._url = url

    def table(self, *args) -> Table:
        """Create a table interface (statfinpy.Table)

        The arguments should be either database and table:
           api.table("StatFin", "statfin_tyokay_pxt_115b.px")
        Or database, level and table:
           api.table("StatFin", "tyokay", "statfin_tyokay_pxt_115b.px")
        """
        assert len(args) in (2, 3)
        return Table(self._concat_url(*args))

    def ls(self, *args) -> pd.DataFrame:
        """Request a content listing as a dataframe

        With no arguments, lists databases
        With one argument (database), lists database layers
        With two arguments (database, layer), lists tables
        """
        return self._get_dataframe(*args)

    def _concat_url(self, *args):
        return "/".join([self._url] + list(args))

    def _get(self, *args):
        r = requests.get(self._concat_url(*args))
        return r.json()

    def _get_dataframe(self, *args):
        j = self._get(*args)
        assert isinstance(j, list)
        assert isinstance(j[0], dict)
        data = {k: [d[k] for d in j] for k in j[0].keys()}
        return pd.DataFrame(data=data)
