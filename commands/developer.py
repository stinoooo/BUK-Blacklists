import discord
from discord.ext import commands
from discord import app_commands
from utils.checks import is_bot_developer

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="eval", description="Evaluate code.")
    @is_bot_developer()
    async def eval(self, interaction: discord.Interaction, code: str):
        # Dangerous eval command for developers only
        try:
            result = eval(code)
            await interaction.response.send_message(f"Result: {result}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="sudo", description="Execute commands as the bot.")
    @is_bot_developer()
    async def sudo(self, interaction: discord.Interaction, command: str):
        # Dangerous sudo command for developers only
        ctx = await self.bot.get_context(interaction)
        await self.bot.process_commands(ctx)

async def setup(bot):
    await bot.add_cog(Developer(bot))
