import os
from discord.ext import commands
import discord

prefix = "!"
bot = commands.Bot(command_prefix=prefix,strip_after_prefix=True,case_insensitive=True,help_command=None,intents=discord.Intents.all(),allowed_mentions=discord.AllowedMentions(everyone=False, replied_user=False))
token = ""
    
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.load_extension("jishaku")
    notToBeLoaded = ['greetHelper.py']
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename not in notToBeLoaded:
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded cog: {filename}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")
bot.run(token)
