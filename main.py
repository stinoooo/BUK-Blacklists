import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from .env
load_dotenv()

# Setup intents
intents = discord.Intents.default()
intents.members = True  # For member updates and joining
intents.guilds = True    # For managing servers
intents.message_content = True  # Required for reading message content if necessary

# Setup bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Load command extensions asynchronously
async def load_extensions():
    await bot.load_extension('commands.moderation')
    await bot.load_extension('commands.admin')
    await bot.load_extension('commands.developer')

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    await bot.change_presence(activity=discord.Game(name="Managing Blacklists"))

    # Sync slash commands for a specific guild for faster testing
    guild_id = os.getenv('GUILD_ID')  # Set the GUILD_ID in your .env file for testing
    if guild_id:
        guild = discord.Object(id=int(guild_id))
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} slash commands to guild {guild_id}.")
    else:
        # Global sync if no GUILD_ID is provided
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands globally.")

# Main entry point
async def main():
    await load_extensions()
    await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())
