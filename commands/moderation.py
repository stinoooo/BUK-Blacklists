import discord
from discord import app_commands
from discord.ext import commands
from utils.checks import is_moderation_team
from utils.database import fetch_blacklist_status

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="check_status", description="Check if a user is blacklisted.")
    @is_moderation_team()
    async def check_status(self, interaction: discord.Interaction, user: discord.User):
        # Fetch blacklist details from MongoDB
        blacklist_record = fetch_blacklist_status(user.id)

        if blacklist_record:
            embed = discord.Embed(
                title="Blacklist Status",
                description=f"{user.mention} is blacklisted.",
                color=discord.Color(0x013a93)
            )
            embed.add_field(name="Reason", value=blacklist_record['reason'], inline=False)
            embed.add_field(name="Blacklisted By", value=f"<@{blacklist_record['blacklisted_by']}>", inline=False)
            embed.add_field(name="Banned Servers", value=", ".join(blacklist_record['banned_servers']), inline=False)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/689530498837381210/1281538937021661254/image.png")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"{user.mention} is not blacklisted.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
