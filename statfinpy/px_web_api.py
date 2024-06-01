import pandas as pd
import requests

from statfinpy.table import Table


class PxWebAPI:
    """Interface to a PxWeb database API"""

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
        url = f"https://statfin.stat.fi/PXWeb/api/v1/{lang}"
        return PxWebAPI(url)

    @staticmethod
    def Verohallinto(lang: str = "fi") -> "PxWebAPI":
        """
        Create an interface to the Tax Administration database

        This database contains statistics about taxation.

        The web interface is located at:
        https://vero2.stat.fi/PXWeb/pxweb/fi/Vero/

        :param str lang: specify the database language (fi/sv/en)
        """
        url = f"https://vero2.stat.fi/PXWeb/api/v1/{lang}"
        return PxWebAPI(url)

    def __init__(self, url: str):
        """Interface to the database located at the given URL"""
        self._url: str = url

    def table(self, *args: str) -> Table:
        """
        Create an interface to a table in this database

        The arguments must locate a specific table in the database, which means
        they must be the names of either a database, a level in that database,
        and a table at that level:

           db.table("StatFin", "tyokay", "statfin_tyokay_pxt_115b.px")

        Or a database and a table in that database:

           api.table("StatFin", "statfin_tyokay_pxt_115b.px")

        The second, shorter form may not work in all API versions.
        """
        assert len(args) in (2, 3)
        return Table(self._concat_url(*args))

    def ls(self, *args: str) -> pd.DataFrame:
        """
        List available contents at various depths

        To list all the databases here, call with no arguments:

            db.ls()

        To list all the layers in a database, call with one argument:

            db.ls("StatFin")

        To list all the tables in a layer, call with two arguments:

            db.ls("StatFin", "tyokay")

        In all cases, the results are returned as a dataframe.
        """
        return self._get_dataframe(*args)

    def _concat_url(self, *args: str) -> str:
        return "/".join([self._url] + list(args))

    def _get(self, *args: str) -> dict | list:
        r = requests.get(self._concat_url(*args))
        return r.json()

    def _get_dataframe(self, *args: str) -> pd.DataFrame:
        j = self._get(*args)
        assert isinstance(j, list)
        assert isinstance(j[0], dict)
        data = {k: [d[k] for d in j] for k in j[0].keys()}
        return pd.DataFrame(data=data)
