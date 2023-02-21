# Cogs

Mel uses [discord.py's cogs](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) in [extensions](https://discordpy.readthedocs.io/en/stable/ext/commands/extensions.html) to allow your bot to be modular to prevent you from having to restart it when you make changes.

Mel has certain commands (in Discord) by default:
- `newext filename`: makes a new file - `cogs/filename.py` and sets up
the basic extension structure with a few imports already at the top.
- `newcog filename cogclassname`: Same as `newext` but it also
creates a cog for you and loads it through the extension system. 
- `load name`: load or reload the extension
- `unload name`: unload the extension
- `extensions`: list status of extensions
- `reloadall`: reload all extensions
- `disableextension name`: prevent an extension from loading on startup
- `enablextension name`: enable a disabled extension
- `tocog`: convenience command to ***attempt*** to help convert non-cog 
commands to cog commands. (ex: converting an existing bot to Mel)
- `sync`: synchronize slash commands with Discord
