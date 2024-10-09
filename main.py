import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Setup intents
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

# Setup bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Load command extensions asynchronously
async def load_extensions():
    await bot.load_extension('commands.moderation')  # Update the path
    await bot.load_extension('commands.admin')       # Update the path
    await bot.load_extension('commands.developer')   # Update the path


@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    await bot.change_presence(activity=discord.Game(name="Managing Blacklists"))
    # Sync slash commands for all guilds
    for guild in bot.guilds:
        await bot.tree.sync(guild=guild)

async def main():
    await load_extensions()
    await bot.start(os.getenv('DISCORD_TOKEN'))

# Entry point
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
