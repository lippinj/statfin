from typing import Any, Iterable
import dataclasses

from statfin.requests import get
from statfin.table import Table


@dataclasses.dataclass
class IndexEntry:
    """Entry in the database index"""

    name: str
    text: str
    typeid: str | None = None

    def __repr__(self):
        """Representational string"""
        fields = [repr(self.name), repr(self.text)]
        if self.typeid:
            fields += [repr(self.typeid)]
        return f"IndexEntry({', '.join(fields)})"

    @staticmethod
    def from_json(j):
        """Parse from JSON"""
        if j is None:
            return None
        elif isinstance(j, list):
            return [IndexEntry.from_json(e) for e in j]
        else:
            name = j.get("id", j.get("dbid", "")).rstrip()
            text = j["text"].rstrip()
            typeid = j.get("type", None)
            if typeid is not None:
                typeid = typeid.rstrip()
            return IndexEntry(name, text, typeid)


class PxWebAPI:
    """Interface to a PxWeb API"""

    def __init__(
        self,
        url: str,
        title: str | None = None,
        j: list | None = None,
    ):
        """Interface to the database located at the given URL"""
        self.url: str = url
        self.title: str | None = title
        self._index: list[IndexEntry] | None = IndexEntry.from_json(j)
        self._cache: dict[str, Any] = {}

    def __repr__(self):
        """Representational string"""
        s = "statfin.PxWebAPI\n"
        s += f"  url: {self.url}\n"
        if self.title:
            s += f"  title: {self.title}\n"
        if len(self.index) == 0:
            s += "  contents: (none)\n"
        else:
            s += "  contents:\n"
            width = max([len(entry.name) for entry in self.index])
            for entry in self.index:
                typeid = entry.typeid if entry.typeid else " "
                name = entry.name.ljust(width)
                s += f"    {typeid} {name} {entry.text}\n"
        return s

    @property
    def index(self):
        """Lazy fetch the index"""
        if self._index is None:
            self._index = IndexEntry.from_json(get(self.url))
        return self._index

    def __iter__(self) -> Iterable[Any]:
        """Iterate databases"""
        for entry in self.index:
            yield self[entry.name]

    def __getattr__(self, name: str) -> Any | Table:
        """Look up database, level or table with the given name"""
        return self[name]

    def __getitem__(self, name: str) -> Any | Table:
        """Look up database, level or table with the given name"""
        entry = self._find_entry(name)
        if entry.name not in self._cache:
            self._cache[entry.name] = self._make_cache(entry)
        return self._cache[entry.name]

    def _make_cache(self, entry):
        url = f"{self.url}/{entry.name}"
        j = get(url)
        if isinstance(j, list):
            return PxWebAPI(url, entry.text, j)
        else:
            return Table(url, j)

    def _find_entry(self, name: str):
        partial_candidates = []
        for entry in self.index:
            if entry.name == name:
                return entry
            elif entry.name == f"{name}.px":
                return entry
            elif name in entry.name:
                partial_candidates.append(entry)

        if len(partial_candidates) == 0:
            raise IndexError(f"No entry {name} or {name}.px in the index")
        elif len(partial_candidates) == 1:
            return partial_candidates[0]
        else:
            raise IndexError(f"Ambiguous partial entry {name} in the index")
