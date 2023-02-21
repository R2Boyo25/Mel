# Config

Mel has two types of configuration included:
- Bot-level configuration
- Guild/server-level configuration

## Bot-level configuration

This configuration is defined in `config.json` and can be 
accessed using `utils.func`'s `config(key)` function.  
You can optionally pass a default value to it, otherwise, 
if there is no value in the config, the bot will just crash 
as it is assumed to be vital to the function of the bot.  
By default Mel has four configuration values:
- `prefix`: a string containing command prefix for if a 
guild doesn't specify one
- `token`: a string containing your bot's token
- `errorChannel`: an integer with the id of the
bot's error channel.
- `logChannel`: and integer with the id of the
bot's log channel.

### IMPORTANT

if sharing code (for example, doing version control with 
`git`),
DO NOT SHARE `config.json` AS IT HAS YOUR BOT'S TOKEN.
Add `config.json` to your `.gitignore` if you're using 
`git`.

## Guild-level configuration

This is available per server and is configured with the 
commands in `cogs/config.py`.  
When you use a custom config value you should add it to 
the set `self.bot.config_options` with `self.bot.config_options.add()`.  
This is used to provide autocompletion to users in slash 
commands; not essential for the bot to function, but nice 
for the users.  

You can access and set config values using the `ServerConf` 
class from `utils.serverconf`. I usually import this as `sc`.  
`ServerConf`'s constructor takes one integer argument: the
id of the server/guild.  
`ServerConf` has four methods:
- `get(key, default, preprocess)`: get a value, default to 
default if no value is found, run preprocess on the value 
if it is found.
- `async` `aget(key, default, async preprocess)`: `aget()`
is the same as `get()` except that it needs to be awaited
and `preprocess` will be called asynchronously. The only 
reason to use `aget` is if you need to do async stuff
in `preprocess`.
- `set(key, value)`: sets `key` to `value` in the config.
- `keys()`: returns an iterator of the keys in the config.
