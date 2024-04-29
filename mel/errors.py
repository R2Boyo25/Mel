from __future__ import annotations

import traceback
import typing
import logging

import discord.ext.commands
import sentry_sdk
from discord import TextChannel
from sentry_sdk.integrations.logging import LoggingIntegration

import mel.mel as mel


class ErrorHandler:
    handlers: dict[str, type["ErrorHandler"]] = {}

    def __init__(self, config: dict[str, typing.Any], mel: mel.Mel):
        self.mel = mel

    async def report(
        self,
        error: BaseException,
        context: dict[str, str] = {},
        user: dict[str, str | int] = {},
    ) -> str | None:
        return print(
            "".join(traceback.format_exception(type(error), error, error.__traceback__))
        )

    async def log(
        self,
        message: str,
        context: dict[str, str] = {},
        user: dict[str, str | int] = {},
        level: typing.Literal[
            "fatal", "critical", "error", "warning", "info", "debug"
        ] = "info",
    ) -> str | None:
        return print(message)

    @classmethod
    def register_handler(cls, name: str, handler: type["ErrorHandler"]) -> None:
        cls.handlers[name] = handler

    @classmethod
    def initialize_handler(
        cls, config: dict[str, typing.Any], mel: mel.Mel
    ) -> "ErrorHandler":
        name: str = config["type"]

        return cls.handlers[name](config, mel)


class DiscordHandler(ErrorHandler):
    def __init__(self, config: dict[str, typing.Any], mel: mel.Mel):
        self.mel = mel
        self.error_channel = config["error_channel"]
        self.log_channel = config["log_channel"]

        logger = logging.getLogger("discord")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename="discord.txt", encoding="utf-8", mode="w"
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        )
        logger.addHandler(handler)

    async def send_embed(
        self,
        title: str,
        body: str,
        channel: int,
        context: dict[str, str] = {},
        user: dict[str, str | int] = {},
    ) -> str | None:
        log = self.mel.bot.get_channel(channel)

        if type(log) is not TextChannel:
            return None

        embed = discord.Embed(
            title=title,
            description="```py\n{}\n```".format(body.replace("```", "\\`\\`\\`")),
            color=0x9C0B21 if title == "Error" else discord.Color.blurple(),
        )

        if "id" in user and "username" in user:
            embed.add_field(name="Author", value=f"{user['id']} (@{user['username']})")

        if "content" in context:
            cleaned_content = context["content"].replace("```", "\\`\\`\\`")
            embed.add_field(name="Message Content", value=f"```{cleaned_content}```")

        message = await log.send(embed=embed)

        return f"[Logged error]({message.jump_url})"

    async def report(
        self,
        error: BaseException,
        context: dict[str, str] = {},
        user: dict[str, str | int] = {},
    ) -> str | None:
        return await self.send_embed(
            "Error",
            "\n".join(traceback.format_exception(error)),
            self.error_channel,
            context,
            user,
        )

    async def log(
        self,
        message: str,
        context: dict[str, str] = {},
        user: dict[str, str | int] = {},
        level: typing.Literal[
            "fatal", "critical", "error", "warning", "info", "debug"
        ] = "info",
    ) -> str | None:
        return await self.send_embed(
            level.title(),
            message,
            self.log_channel if level == "info" else self.error_channel,
            context,
            user,
        )


class SentryHandler(ErrorHandler):
    def __init__(self, config: dict[str, typing.Any], mel: mel.Mel):
        self.mel = mel
        config.pop("type")

        logging.getLogger("discord").setLevel(logging.INFO)

        sentry_sdk.init(**config)

    async def report(
        self,
        error: BaseException,
        context: dict[str, str] = {},
        user: dict[str, str | int] = {},
    ) -> str | None:
        sentry_sdk.set_user(user)
        sentry_sdk.set_context("message", context)
        event_id = sentry_sdk.capture_exception(error)

        if event_id is None:
            return None

        return f"Event id: {event_id}"

    async def log(
        self,
        message: str,
        context: dict[str, str] = {},
        user: dict[str, str | int] = {},
        level: typing.Literal[
            "fatal", "critical", "error", "warning", "info", "debug"
        ] = "info",
    ) -> str | None:
        sentry_sdk.set_user(user)
        sentry_sdk.set_context("message", context)
        event_id = sentry_sdk.capture_message(message, level)

        if event_id is None:
            return None

        return f"Event id: {event_id}"


ErrorHandler.register_handler("discord", DiscordHandler)
ErrorHandler.register_handler("sentry", SentryHandler)
