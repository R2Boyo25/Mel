import json
import os
from typing import Any, Optional, Self, cast
from hippodb_client import AuthenticatedHippo


HIPPODB = cast(AuthenticatedHippo, None)


class JSONDatabase(object):
    def __init__(self, location: str):
        location = location.replace("~/", "")
        self.database_path = "/" + "/".join(location.split("/")[:-1])
        self.document_name = location.split("/")[-1]

    async def load(self) -> Self:
        if await HIPPODB.document_exists(self.database_path, self.document_name):
            self.db = cast(
                dict[str, Any],
                await HIPPODB.read_document(self.database_path, self.document_name),
            )

        else:
            await HIPPODB.create_document(self.database_path, self.document_name, {})
            self.db: dict[Any, Any] = {}

        return self

    async def dumpdb(self) -> None:
        await HIPPODB.update_document(self.database_path, self.document_name, self.db)

    async def set(self, key: str | int | float | bool, value: Any) -> None:
        self.db[str(key)] = value
        await self.dumpdb()

    async def get(self, key: str, default: Optional[Any] = None) -> Any:
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

    async def pop(self, key: str) -> Any:
        a = self.db.pop(key)
        await self.dumpdb()

        return a

    def keys(self) -> list[str]:
        return list(self.db.keys())


class JSONFile(object):
    def __init__(self, location: str):
        self.location = os.path.expanduser(location)

        if os.path.exists(self.location):
            self.db = json.load(open(self.location, "r"))

        else:
            self.db: dict[Any, Any] = {}

    def dumpdb(self) -> None:
        json.dump(self.db, open(self.location, "w+"), indent=4)

    def set(self, key: str | int | float | bool, value: Any) -> None:
        self.db[str(key)] = value
        self.dumpdb()

    def get(self, key: str, default: Optional[Any] = None) -> Any:
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

    def pop(self, key: str) -> Any:
        a = self.db.pop(key)
        self.dumpdb()

        return a

    def keys(self) -> Any:
        return self.db.keys()
