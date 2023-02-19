import json
import os
from typing import Any, Optional


class JSONDatabase(object):
    def __init__(self, location: str):
        self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self, location: str) -> None:
        if os.path.exists(location):
            self._load()
        else:
            self.db = {}

    def _load(self) -> None:
        self.db = json.load(open(self.location, "r"))

    def dumpdb(self) -> None:
        json.dump(self.db, open(self.location, "w+"), indent=4)

    def set(self, key: str, value: Any) -> None:
        self.db[str(key)] = value
        self.dumpdb()

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        if key not in self.db:
            if default:
                return default

            raise ValueError(f"No value set for {key} in DB and no default value passed to get()")
        
        return self.db[key]

    def delete(self, key: str) -> None:
        if not key in self.db:
            return
        del self.db[key]
        self.dumpdb()

    def resetdb(self) -> None:
        self.db = {}
        self.dumpdb()

    def pop(self, key: str) -> Any:
        a = self.db.pop(key)
        self.dumpdb()

        return a

    def keys(self) -> Any:
        return self.db.keys()
