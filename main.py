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

    # Sync globally
    synced_commands = await bot.tree.sync()
    print(f"Global slash commands synced: {len(synced_commands)} commands available.")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Check if it's a DM
    if isinstance(message.channel, discord.DMChannel):
        # Create an embed
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

# Main entry point
async def main():
    await load_extensions()
    await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())
