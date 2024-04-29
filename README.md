# Mel

## So, what is Mel and why did you make it?

Mel is a library that I extracted from my first discord bot and have maintained over time.
It's made up of code that was common to a lot of the discord bots I was making.

## How do I install it?

```bash
# Replace the path with the install location for Mel
git clone https://github.com/R2Boyo25/Mel /path/to/where/you/want/to/install/Mel
```

### Configuration

TODO

## Making your bot

Like with every bot, you first have to make a bot through the Discord Developer Portal,
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
