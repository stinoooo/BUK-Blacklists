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

# Load command extensions
bot.load_extension('bot.commands.moderation')
bot.load_extension('bot.commands.admin')
bot.load_extension('bot.commands.developer')

# Event when bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    await bot.change_presence(activity=discord.Game(name="Managing Blacklists"))
    # Sync slash commands
    for guild in bot.guilds:
        await bot.tree.sync(guild=guild)

# Run bot
bot.run(os.getenv('DISCORD_TOKEN'))
