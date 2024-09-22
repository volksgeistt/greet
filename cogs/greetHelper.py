import json
import discord
import re

class GreetHelper:
    @staticmethod
    def load_data():
        try:
            with open('greet_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_data(data):
        with open('greet_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def is_valid_url(url):
        urlPattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return bool(urlPattern.match(url))

    @staticmethod
    async def format_message(user, message):
        greetVariable = message
        greetVariable = greetVariable.replace("{user}", str(user))
        greetVariable = greetVariable.replace("{user.mention}", user.mention)
        greetVariable = greetVariable.replace("{user.name}", user.name)
        greetVariable = greetVariable.replace("{user.joined_at}", discord.utils.format_dt(user.joined_at, style="R"))
        greetVariable = greetVariable.replace("{guild.name}", user.guild.name)
        greetVariable = greetVariable.replace("{guild.count}", str(user.guild.member_count))
        greetVariable = greetVariable.replace("{guild.id}", str(user.guild.id))
        greetVariable = greetVariable.replace("{guild.created_at}", discord.utils.format_dt(user.guild.created_at, style="R"))
        greetVariable = greetVariable.replace("{guild.boost_count}", str(user.guild.premium_subscription_count))
        greetVariable = greetVariable.replace("{guild.boost_tier}", str(user.guild.premium_tier))
        return greetVariable

    @staticmethod
    async def format_field(user, text):
        if not text:
            return ""
        return await GreetHelper.format_message(user, text)

    @staticmethod
    async def send_greet_message(channel, user, guild_data):
        message = guild_data.get('message', 'Welcome to the server, {user.mention}!')
        formatted_message = await GreetHelper.format_message(user, message)
        if guild_data.get('use_embed', False):
            embed = discord.Embed(description=formatted_message, color=discord.Color.green())
            if 'title' in guild_data:
                embed.title = await GreetHelper.format_field(user, guild_data['title'])
            if 'footer' in guild_data:
                footer_text = await GreetHelper.format_field(user, guild_data['footer'])
                embed.set_footer(text=footer_text)
            if 'image' in guild_data:
                embed.set_image(url=guild_data['image'])
            if 'thumbnail' in guild_data:
                embed.set_thumbnail(url=guild_data['thumbnail'])
            if guild_data.get('ping', False):
                await channel.send(user.mention, embed=embed)
            else:
                await channel.send(embed=embed)
        else:
            await channel.send(formatted_message)
