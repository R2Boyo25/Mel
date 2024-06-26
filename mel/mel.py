import asyncio
from dataclasses import dataclass, field
import typing

import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from hippodb_client import AppID, AuthenticatedHippo, HippoToken
from pydantic import BaseModel
from yarl import URL

from mel.utils.jdb import JSONDatabase, JSONFile
import mel.utils.jdb
from .errors import ErrorHandler


class _ConfigError(Exception):
    pass


class HippoDBConfig(BaseModel):
    url: str
    app_id: str
    token: str


@dataclass
class Mel:
    bot: Bot
    config_options: set[str] = field(default_factory=set)
    mel_config: JSONFile[typing.Any] = JSONFile("config")
    hippodb_config = HippoDBConfig(**mel_config.get("hippodb_config"))
    error_handler: ErrorHandler = None  # type: ignore

    def __post_init__(self) -> None:
        if self.error_handler is None:
            self.error_handler = ErrorHandler.initialize_handler(
                self.mel_config.get("logging"), self
            )

    def config(
        self, key: str, default: typing.Optional[typing.Any] = None
    ) -> typing.Any:
        try:
            if key in self.mel_config.keys():
                return self.mel_config.get(key, default)

            if default is not None:
                return default

            raise _ConfigError(
                f"Config missing {key} and no default passed to config()"
            )

        except _ConfigError as e:
            print(e)
            quit()

    async def get_prefix(
        self, bot: commands.Bot, message: discord.Message
    ) -> list[str]:
        prefix: list[str] | str = self.config("default_bot_prefix")

        if not message.guild:
            # No prefix in dms
            return []

        prefix_db: JSONDatabase[list[str] | str] = await JSONDatabase.load("prefixes")

        if str(message.guild.id) in prefix_db.keys():
            prefixes = await prefix_db.get(str(message.guild.id))

        elif type(prefix) is list:
            prefixes = prefix

        else:
            prefixes = [prefix]  # type: ignore

        # If we are in a guild, we allow for the user to mention us or use the custom prefix.
        return commands.when_mentioned_or(*prefixes)(self.bot, message)

    async def _init_async(self) -> None:
        mel.utils.jdb.HIPPODB = await AuthenticatedHippo.create(
            URL(self.hippodb_config.url),
            AppID(self.hippodb_config.app_id),
            HippoToken(self.hippodb_config.token),
        )

        try:
            await self.bot.start(self.config("token"))

        except KeyboardInterrupt:
            await mel.utils.jdb.HIPPODB.close()

    def start(self) -> None:
        asyncio.run(self._init_async())
