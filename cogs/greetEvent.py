from discord.ext import commands
from .greetHelper import GreetHelper

class GreetEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.greet_data = GreetHelper.load_data()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        if guild_id not in self.greet_data:
            return
        guild_data = self.greet_data[guild_id]
        channel_id = guild_data.get('channel')
        if not channel_id:
            return
        channel = self.bot.get_channel(channel_id)
        if not channel:
            return
        await GreetHelper.send_greet_message(channel, member, guild_data)

async def setup(bot):
    await bot.add_cog(GreetEvent(bot))
        
        
    
