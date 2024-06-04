import pandas as pd
import requests

from statfin.table import Table


class PxWebAPI:
    """Interface to a PxWeb API"""

    @staticmethod
    def StatFin(lang: str = "fi") -> "PxWebAPI":
        """
        Create an interface to the StatFin database

        This is the main database of Statistics Finland, and contains various
        statistics about the Finnish society and population.

        The web interface is located at:
        https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/

        :param str lang: specify the database language (fi/sv/en)
        """
        return PxWebAPI("https://statfin.stat.fi/PXWeb/api", "v1", lang)

    @staticmethod
    def Verohallinto(lang: str = "fi") -> "PxWebAPI":
        """
        Create an interface to the Tax Administration database

        This database contains statistics about taxation.

        The web interface is located at:
        https://vero2.stat.fi/PXWeb/pxweb/fi/Vero/

        :param str lang: specify the database language (fi/sv/en)
        """
        return PxWebAPI("https://vero2.stat.fi/PXWeb/api", "v1", lang)

    def __init__(self, root: str, version: str, language: str):
        """Interface to the database located at the given URL"""
        self._root: str = root
        self._version: str = version
        self._language: str = language

    def table(self, *args: str) -> Table:
        """
        Create an interface to a specific table

        The arguments must constitute a path to a specific table, starting with
        the database ID and ending with the table name (with any levels in
        between):

           db.table("StatFin", "tyokay", "statfin_tyokay_pxt_115b.px")

        In some versions of the API, you can skip the levels, just specifying
        the database ID and the table name:

           api.table("StatFin", "statfin_tyokay_pxt_115b.px")
        """
        assert len(args) >= 2
        return Table(self._concat_url(*args))

    def ls(self, *args: str) -> pd.DataFrame:
        """
        List available contents at various depths

        To list all the databases here, call with no arguments:

            db.ls()

        To list content inside a database (levels or tables), call with one or
        more arguments:

            db.ls("StatFin")
            db.ls("StatFin", "tyokay")

        In all cases, the results are returned as a dataframe.
        """
        return self._get_as_dataframe(*args)

    def _concat_url(self, *args: str) -> str:
        """Concatenate the base URL and args into an endpoint URL"""
        return "/".join([self._root, self._version, self._language] + list(args))

    def _get(self, *args: str) -> dict | list:
        """HTTP GET the concatenation of args"""
        r = requests.get(self._concat_url(*args))
        return r.json()

    def _get_as_dataframe(self, *args: str) -> pd.DataFrame:
        """Like _get(), but forms the response into a dataframe"""
        j = self._get(*args)
        assert isinstance(j, list)
        assert isinstance(j[0], dict)
        data = {k: [d[k] for d in j] for k in j[0].keys()}
        return pd.DataFrame(data=data)
