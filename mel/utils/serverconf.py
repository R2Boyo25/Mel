from mel.utils.jdb import JSONDatabase, T
import os
from typing import Any, Callable, Coroutine, Generic, Optional, TypeVar


class ServerConf(Generic[T]):
    def __init__(self, guildid: int):
        self.guildid = guildid
        self.confpath = f"configs/{guildid}"

    async def get(
        self,
        key: str,
        default: T | None = None,
        preprocess: Optional[Callable[[Any], Coroutine[Any, Any, T]]] = None,
    ) -> T:
        if not os.path.exists(self.confpath):
            if default is None:
                raise ValueError(
                    f"No value set for {key} in {self.guildid} and no default value passed to ServerConf.get()"
                )

            return default

        cdb: JSONDatabase[T] = await JSONDatabase.load(self.confpath)

        if key not in cdb.keys():
            if default is None:
                raise ValueError(
                    f"No value set for {key} in {self.guildid} and no default value passed to ServerConf.get()"
                )

            return default

        if preprocess is not None:
            return await preprocess(cdb.get(key))

        return await cdb.get(key)

    async def set(self, key: str, value: T) -> None:
        if not os.path.exists("configs"):
            os.mkdir("configs")

        if not os.path.exists(self.confpath):
            with open(self.confpath, "w") as f:
                f.write("{}")

        cdb: JSONDatabase[T] = await JSONDatabase.load(self.confpath)

        if value is None:
            if key in cdb.keys():
                await cdb.delete(key)

            return

        await cdb.set(key, value)
