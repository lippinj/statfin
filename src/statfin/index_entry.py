import dataclasses


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
