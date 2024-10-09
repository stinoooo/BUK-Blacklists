import discord
from discord import app_commands
from discord.ext import commands
from utils.checks import is_moderation_or_admin
from utils.database import fetch_blacklist_status, edit_blacklist_reason  # Ensure edit function is defined

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="check status", description="Check if a user is blacklisted.")
    @is_moderation_or_admin()
    async def check_status(self, interaction: discord.Interaction, user: discord.User):
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
            embed.add_field(name="Case ID", value=blacklist_record['case_id'], inline=False)  # Include case ID
            embed.add_field(name="Date", value=blacklist_record['date_blacklisted'].strftime("%Y-%m-%d %H:%M:%S"), inline=False)  # Include date
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/689530498837381210/1281538937021661254/image.png")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"{user.mention} is not blacklisted.", ephemeral=True)

    @app_commands.command(name="lookup user", description="Lookup a user and show their roles in shared servers.")
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
            await interaction.response.send_message(f"{user.mention} is not in any shared servers.", ephemeral=True)

    @app_commands.command(name="edit reason", description="Edit the reason for a blacklist case.")
    @is_moderation_or_admin()
    async def edit_reason(self, interaction: discord.Interaction, case_id: int, new_reason: str):
        success = edit_blacklist_reason(case_id, new_reason)  # Ensure this function updates the reason in the database
        if success:
            await interaction.response.send_message(f"Successfully updated reason for case ID: {case_id}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Failed to update reason for case ID: {case_id}.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))