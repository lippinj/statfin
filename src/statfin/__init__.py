from statfin.px_web_api import PxWebAPI
from statfin.query import Query
from statfin.requests import RequestError
from statfin.table import Table
from statfin.variable import Variable, Value
from statfin import cache


def StatFin(lang: str = "fi") -> PxWebAPI:
    """
    Create an interface to the StatFin database

    This is the main database of Statistics Finland, and contains various
    statistics about the Finnish society and population.

    The web interface is located at:
    https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/

    :param str lang: specify the database language (fi/sv/en)
    """
    return PxWebAPI(f"https://statfin.stat.fi/PXWeb/api/v1/{lang}")


def Vero(lang: str = "fi") -> PxWebAPI:
    """
    Create an interface to the Tax Administration database

    This database contains statistics about taxation.

    The web interface is located at:
    https://vero2.stat.fi/PXWeb/pxweb/fi/Vero/

    :param str lang: specify the database language (fi/sv/en)
    """
    return PxWebAPI(f"https://vero2.stat.fi/PXWeb/api/v1/{lang}")
