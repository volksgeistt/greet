import discord
from discord.ext import commands
from .greetHelper import GreetHelper
import re
class GreetCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.greet_data = GreetHelper.load_data()

    def save_data(self):
        GreetHelper.save_data(self.greet_data)

    @commands.group(name='greet', invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def greet(self, ctx):
        await ctx.send("❌ Please use valid subcommands available in the bot to manage the greet system!")

    @greet.command(name='channel')
    @commands.has_permissions(manage_guild=True)
    async def greet_channel(self, ctx, action: str, channel: discord.TextChannel = None):
        guild_id = str(ctx.guild.id)
        if action.lower() == 'add':
            if channel:
                self.greet_data.setdefault(guild_id, {})['channel'] = channel.id
                await ctx.send(f"✅ Greet channel set to {channel.mention}")
            else:
                await ctx.send("❌ OOPS! You forgot to specify a channel.")
        elif action.lower() == 'remove':
            if guild_id in self.greet_data and 'channel' in self.greet_data[guild_id]:
                del self.greet_data[guild_id]['channel']
                await ctx.send("✅ Greet channel removed.")
            else:
                await ctx.send("❌ Greet channel doesn't exist for this server!")
        elif action.lower() == 'show':
            channel_id = self.greet_data.get(guild_id, {}).get('channel')
            if channel_id:
                channel = ctx.guild.get_channel(channel_id)
                await ctx.send(f"Currently greet is enabled in {channel.mention}")
            else:
                await ctx.send("❌ Greet channel doesn't exist for this server!")
        else:
            await ctx.send("❌ Invalid Greet Action.! Use 'add', 'remove', or 'show'.")
            
        self.save_data()

    @greet.command(name='embed')
    @commands.has_permissions(manage_guild=True)
    async def greet_embed(self, ctx):
        guild_id = str(ctx.guild.id)
        self.greet_data.setdefault(guild_id, {})['use_embed'] = not self.greet_data[guild_id].get('use_embed', False)
        await ctx.send(f"✅ Greet embed has been {'enabled' if self.greet_data[guild_id]['use_embed'] else 'disabled'}.")
        self.save_data()

    @greet.command(name='footer')
    @commands.has_permissions(manage_guild=True)
    async def greet_footer(self, ctx, *, text: str):
        guild_id = str(ctx.guild.id)
        self.greet_data.setdefault(guild_id, {})['footer'] = text
        await ctx.send(f"✅ Greet footer has been set.")
        self.save_data()

    @greet.command(name='message')
    @commands.has_permissions(manage_guild=True)
    async def greet_message(self, ctx, *, message: str):
        guild_id = str(ctx.guild.id)
        self.greet_data.setdefault(guild_id, {})['message'] = message
        await ctx.send(f"✅ Greet message has been set and updated to the database for this guild.")
        self.save_data()

    @greet.command(name='ping')
    @commands.has_permissions(manage_guild=True)
    async def greet_ping(self, ctx):
        guild_id = str(ctx.guild.id)
        self.greet_data.setdefault(guild_id, {})['ping'] = not self.greet_data[guild_id].get('ping', False)
        await ctx.send(f"✅ Greet ping has been {'enabled' if self.greet_data[guild_id]['ping'] else 'disabled'}.")
        self.save_data()

    @greet.command(name='image')
    @commands.has_permissions(manage_guild=True)
    async def greet_image(self, ctx, url: str):
        if not self.is_valid_url(url):
            await ctx.send("❌ Please provide a valid URL for greet image.")
            return
        
        guild_id = str(ctx.guild.id)
        self.greet_data.setdefault(guild_id, {})['image'] = url
        await ctx.send(f"✅ Greet image has been set.")
        self.save_data()

    @greet.command(name='thumbnail')
    @commands.has_permissions(manage_guild=True)
    async def greet_thumbnail(self, ctx, url: str):
        if not self.is_valid_url(url):
            await ctx.send("❌ Please provide a valid URL for greet thumbnail.")
            return
        
        guild_id = str(ctx.guild.id)
        self.greet_data.setdefault(guild_id, {})['thumbnail'] = url
        await ctx.send(f"✅ Greet thumbnail has been set.")
        self.save_data()

    @greet.command(name='title')
    @commands.has_permissions(manage_guild=True)
    async def greet_title(self, ctx, *, title: str):
        guild_id = str(ctx.guild.id)
        self.greet_data.setdefault(guild_id, {})['title'] = title
        await ctx.send(f"✅ Greet title has been set.")
        self.save_data()

    @greet.command(name='test')
    @commands.has_permissions(manage_guild=True)
    async def greet_test(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.greet_data:
            await ctx.send("❌ Greet system is not set up for this guild.")
            return

        guild_data = self.greet_data[guild_id]
        channel_id = guild_data.get('channel')
        if not channel_id:
            await ctx.send("❌ Greet channel is not set in this guild. Please set a greet channel first.")
            return

        channel = ctx.guild.get_channel(channel_id)
        if not channel:
            await ctx.send("❌ The set greet channel no longer exists. Please set a new greet channel.")
            return

        await GreetHelper.send_greet_message(channel, ctx.author, guild_data)
        await ctx.send(f"✅ Tested greet message in {channel.mention}")

async def setup(bot):
    await bot.add_cog(GreetCommands(bot))
