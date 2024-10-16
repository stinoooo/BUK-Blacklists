import discord
from discord import app_commands
from discord.ext import commands
from utils.checks import is_moderation_or_admin
from utils.database import fetch_blacklist_status, edit_blacklist_reason

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="check-status", description="Check if a user is blacklisted.")
    @app_commands.check(is_moderation_or_admin)
    async def check_status(self, interaction: discord.Interaction, user: discord.User):
        # Fetch blacklist record by user ID
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
            embed.add_field(name="Case ID", value=blacklist_record['case_id'], inline=False)
            embed.add_field(name="Date", value=blacklist_record['date_blacklisted'].strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/689530498837381210/1281538937021661254/image.png")
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="Blacklist Status",
                description=f"{user.mention} is not blacklisted.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="lookup-user", description="Lookup a user and show their roles in shared servers.")
    @is_moderation_or_admin()
    async def lookup_user(self, interaction: discord.Interaction, user: discord.User):
        servers_info = []
        for guild in self.bot.guilds:
            if user in guild.members:
                roles = [role.name for role in user.roles if role.guild.id == guild.id]
                servers_info.append(f"**{guild.name}**: Roles - {', '.join(roles)}")

        if servers_info:
            embed = discord.Embed(
                title=f"{user}'s Roles in Shared Servers",
                description="\n".join(servers_info),
                color=discord.Color(0x013a93)
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="Lookup User",
                description=f"{user.mention} is not in any shared servers.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="edit-reason", description="Edit the reason for a blacklist case.")
    @app_commands.check(is_moderation_or_admin)
    async def edit_reason(self, interaction: discord.Interaction, case_id: int, new_reason: str):
        success = edit_blacklist_reason(case_id, new_reason)
        if success:
            embed = discord.Embed(
                title="Edit Reason",
                description=f"Successfully updated reason for case ID: {case_id}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="Edit Reason",
                description=f"Failed to update reason for case ID: {case_id}.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))