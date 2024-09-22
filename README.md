# discordGreet
- A customizable greeting system for Discord servers, built using Discord.py.
# Features:
- Customizable welcome messages
- Embed support with customizable fields
- Channel selection for greetings
- User mention toggle
- Custom images and thumbnails
- Easy-to-use command system for server administrators
## greetCommands:
- `greet channel <add/remove/show> [#channel]` - Manage the greeting channel
- `greet embed` - Toggle embed usage
- `greet footer <text>` - Set the footer text for embeds
- `greet ping` - Toggle user pinging in greetings
- `greet image <url>` - Set the image for embeds
- `greet thumbnail <url>` - Set the thumbnail for embeds
- `greet title <text>` - Set the title for embeds
- `greet test` - Test the current greeting configuration
## greetMessage Variables:
- `{user}` - User's full name and discriminator
- `{user.mention}` - Mentions the user
- `{user.name}` - User's name
- `{user.joined_at}` - When the user joined the server
- `{guild.name}` - Server name
- `{guild.count}` - Server member count
- `{guild.id}` - Server ID
- `{guild.created_at}` - When the server was created
- `{guild.boost_count}` - Number of server boosts
- `{guild.boost_tier}` - Server boost tier
## greetConfig:
The bot stores greeting configurations for each server in a greet_data.json file. This file is automatically created and updated as you use the bot commands.
## Acknowledgments:
Discord.py (https://github.com/Rapptz/discord.py) - The Python library used for interacting with the Discord API







