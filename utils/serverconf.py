from utils.jdb import JSONDatabase as jdb
import os
from typing import Any, Callable, Optional


class ServerConf:
    def __init__(self, guildid: int):
        self.guildid = guildid
        self.confpath = f"configs/{guildid}.json"

    def get(
        self,
        key: str,
        default: Any = None,
        preprocess: Optional[Callable[[Any], Any]] = None,
    ) -> Any:
        if not os.path.exists(self.confpath):
            if default is None:
                raise ValueError(
                    f"No value set for {key} in {self.guildid} and no default value passed to ServerConf.get()"
                )

            return default

        cdb = jdb(self.confpath)

        if key not in cdb.keys():
            if default is None:
                raise ValueError(
                    f"No value set for {key} in {self.guildid} and no default value passed to ServerConf.get()"
                )

            return default

        if preprocess is not None:
            return preprocess(cdb.get(key))

        return cdb.get(key)

    async def get(
        self,
        key: str,
        default: Any = None,
        preprocess: Optional[Callable[[Any], Any]] = None,
    ) -> Any:
        if not os.path.exists(self.confpath):
            if default is None:
                raise ValueError(
                    f"No value set for {key} in {self.guildid} and no default value passed to ServerConf.get()"
                )

            return default

        cdb = jdb(self.confpath)

        if key not in cdb.keys():
            if default is None:
                raise ValueError(
                    f"No value set for {key} in {self.guildid} and no default value passed to ServerConf.get()"
                )

            return default

        if preprocess is not None:
            return await preprocess(cdb.get(key))

        return cdb.get(key)
    
    def set(self, key: str, value: Any) -> None:
        if not os.path.exists("configs"):
            os.mkdir("configs")

        if not os.path.exists(self.confpath):
            with open(self.confpath, "w") as f:
                f.write("{}")

        cdb = jdb(self.confpath)

        if value is None:
            if key in cdb.keys():
                cdb.delete(key)
            return

        cdb.set(key, value)
