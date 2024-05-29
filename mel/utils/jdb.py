import json
import os
from typing import Any, Generic, Optional, Self, TypeVar, cast
from hippodb_client import AuthenticatedHippo
from pydantic import Json


HIPPODB = cast(AuthenticatedHippo, None)
T = TypeVar("T")  # , str, dict[str, Any], list[Any], int, float, bool, None


class JSONDatabase(Generic[T]):
    def __init__(self, /, _is_from_internal: bool = False):
        if not _is_from_internal:
            raise NotImplementedError("Use `await JSONDatabase.load()` instead.")

        self.database_path: str
        self.document_name: str
        self.db: dict[str, T]

    @classmethod
    async def load(cls, location: str) -> Self:
        self = cls()

        location = location.replace("~/", "")
        self.database_path = "/" + "/".join(location.split("/")[:-1])
        self.document_name = location.split("/")[-1]

        if await HIPPODB.document_exists(self.database_path, self.document_name):
            self.db = cast(
                dict[str, Any],
                await HIPPODB.read_document(self.database_path, self.document_name),
            )

        else:
            await HIPPODB.create_document(self.database_path, self.document_name, {})
            self.db = {}

        return self

    async def dumpdb(self) -> None:
        await HIPPODB.update_document(self.database_path, self.document_name, self.db)

    async def set(self, key: str | int | float | bool, value: T) -> None:
        self.db[str(key)] = value
        await self.dumpdb()

    async def get(self, key: str, default: T | None = None) -> T:
        if key not in self.db:
            if default is None:
                raise ValueError(
                    f"No value set for {key} in DB and no default value passed to get()"
                )

            return default

        return self.db[key]

    async def delete(self, key: str) -> None:
        if not key in self.db:
            return
        del self.db[key]
        await self.dumpdb()

    async def resetdb(self) -> None:
        self.db = {}
        await self.dumpdb()

    async def pop(self, key: str) -> T:
        a = self.db.pop(key)
        await self.dumpdb()

        return a

    def keys(self) -> list[str]:
        return list(self.db.keys())


class JSONFile(Generic[T]):
    def __init__(self, location: str):
        self.location = os.path.expanduser(location)
        self.db: dict[str, T]

        if os.path.exists(self.location):
            self.db = json.load(open(self.location, "r"))

        else:
            self.db = {}

    def dumpdb(self) -> None:
        json.dump(self.db, open(self.location, "w+"), indent=4)

    def set(self, key: str | int | float | bool, value: T) -> None:
        self.db[str(key)] = value
        self.dumpdb()

    def get(self, key: str, default: Optional[T] = None) -> T:
        if key not in self.db:
            if default is None:
                raise ValueError(
                    f"No value set for {key} in DB and no default value passed to get()"
                )

            return default

        return self.db[key]

    def delete(self, key: str) -> None:
        if not key in self.db:
            return

        del self.db[key]
        self.dumpdb()

    def resetdb(self) -> None:
        self.db = {}
        self.dumpdb()

    def pop(self, key: str) -> T:
        a = self.db.pop(key)
        self.dumpdb()

        return a

    def keys(self) -> list[str]:
        return list(self.db.keys())
