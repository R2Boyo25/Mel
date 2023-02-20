# Mel

## So, what is Mel and why did you make it?

Mel is a collection of code I extracted from my main discord bot to use 
to develop my other discord bots on top of.  
It is designed to allow you to work completely on cogs without touching 
the bot part of the bot, allowing complete modularity.  

I have not tested this on Windows or Mac but it does work on Gentoo and Debian
so it should work on most linux systems with a working Python 3 install.  
It works entirely in a virtual environment and does some *admittedly weird*
stuff with the virtualenv to load its packages from the existing python interpreter.  
It then adds the path of your code to itself so that it canload your cogs 
as if they were part of the bot itself.  

## How do I install it?

The easiest method is to install it using my package manager, 
[Avalon Package Manager](https://github.com/R2Boyo25/AvalonPackageManager):

```bash
# install APM
cd /tmp
git clone https://github.com/R2Boyo25/AvalonPackageManager apm
cd apm
python3 install.py
cd ..
rm -r apm

# install Mel
apm install r2boyo25/mel

# and later, update Mel
apm update r2boyo25/mel
```

but I think most people don't want to do that, so you can also just clone the repository:

```bash
# Replace the path with the install location for Mel
git clone https://github.com/R2Boyo25/Mel /path/to/where/you/want/to/install/Mel
```

## Making your bot
Like with every bot you first have to make a bot through the Discord Developer Portal,
but there's already tutorials on that so you can find out how to do that yourself.  
You do need to enable the Message Content Intent in the bot for non-slash-commands 
commands to work.  

Before you can run your bot, you first have
to make the code for it.

```
# Make the directory for your bot
mkdir /path/to/your/bot

# Copying the included example cogs to provide a base
cp -r /path/to/mel/cogs /path/to/your/bot

# Copy the requirements file for the bot's dependencies.
cp /path/to/mel/requirements.txt.example /path/to/your/bot/requirements.txt

# Generating the config.json file
## this will also make a virtual environment
## and install dependencies into it.
python3 /path/to/mel/bot.py /path/to/your/bot

### Edit the generated config file in your editor ###
# BTW that thing at the beginning just tries to get your preferred
# editor and defaults to `nano`
${VISUAL_EDITOR-${VISUAL-${EDITOR-nano}}} /path/to/your/bot/config.json
```

And you should now have a basic bot setup!

## Running your bot
```bash
python3 /path/to/mel/bot.py /path/to/your/bot
```

And now you should have your bot connected to discord and responding to commands 
with the prefix you specified earlier.
