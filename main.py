import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import logging

# Load environment variables from .env
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setup intents
intents = discord.Intents.default()
intents.members = True  # For member updates and joining
intents.guilds = True    # For managing servers
intents.message_content = True  # Required for reading message content if necessary

# Setup bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Logging channel ID
LOG_CHANNEL_ID = 1293589581643386881

async def send_log(message: str):
    """Sends log messages to the specified log channel."""
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(message)
    else:
        logger.error("Log channel not found.")

# Load command extensions asynchronously
async def load_extensions():
    try:
        await bot.load_extension('commands.general')
        await bot.load_extension('commands.moderation')
        await bot.load_extension('commands.admin')
        await bot.load_extension('commands.developer')
        logger.info("Extensions loaded successfully.")
    except Exception as e:
        await send_log(f"Failed to load extensions: {e}")
        logger.error(f"Failed to load extensions: {e}")

@bot.event
async def on_ready():
    logger.info(f'{bot.user} is online!')
    await bot.change_presence(activity=discord.Game(name="Managing Blacklists"))

    # Sync globally
    synced_commands = await bot.tree.sync()
    logger.info(f"Global slash commands synced: {len(synced_commands)} commands available.")

@bot.event
async def on_guild_join(guild):
    # Log information when the bot joins a new guild
    logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")
    permissions = guild.me.guild_permissions
    invite_link = await guild.text_channels[0].create_invite(max_age=3600)  # 1-hour invite link

    embed = discord.Embed(
        title="Bot Added to Server",
        description=f"The bot has been added to **{guild.name}**.",
        color=discord.Color.green()
    )
    embed.add_field(name="Invited By", value=f"<@{guild.me.id}>", inline=False)
    embed.add_field(name="Permissions", value=", ".join([perm for perm, value in permissions if value]), inline=False)
    embed.add_field(name="Invite Link", value=f"[Click Here]({invite_link})", inline=False)
    
    await send_log(embed)

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Check if it's a DM
    if isinstance(message.channel, discord.DMChannel):
        embed = discord.Embed(
            title="Direct Messages Not Supported",
            description="We are unable to respond to direct messages sent to this bot. If you need assistance or wish to contact the BUK Moderation Team, "
                        "please feel free to reach out to them directly via Modmail by clicking the button below.",
            color=discord.Color.blue()
        )
        
        # Create a button that leads to the modmail channel
        view = discord.ui.View()
        button = discord.ui.Button(label="Contact BUK Modmail", url="https://discordapp.com/channels/@me/1282748337711353927", style=discord.ButtonStyle.link)
        view.add_item(button)
        
        # Send the embed and button as a response
        await message.channel.send(embed=embed, view=view)

@bot.event
async def on_command(ctx):
    """Logs the usage of commands."""
    logger.info(f"Command used: {ctx.command} by {ctx.author} in {ctx.channel}")
    await send_log(f"Command used: **{ctx.command}** by **{ctx.author}** in **{ctx.channel}**.")

@bot.event
async def on_command_error(ctx, error):
    """Logs errors related to commands."""
    logger.error(f"Error in command {ctx.command}: {error}")
    
    # Check if the error is sensitive
    if isinstance(error, discord.NotFound) or "missing permissions" in str(error).lower():
        await send_log(f"Error in command **{ctx.command}**: An issue occurred. Please check the console for details.")
    else:
        await send_log(f"Error in command **{ctx.command}**: {error}")

@bot.event
async def on_error(event, *args, **kwargs):
    """Logs errors that occur outside of commands."""
    logger.error(f"An error occurred in event {event}: {args}, {kwargs}")
    await send_log(f"An error occurred in event **{event}**: Please check the console for details.")

# Main entry point
async def main():
    await load_extensions()
    await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())