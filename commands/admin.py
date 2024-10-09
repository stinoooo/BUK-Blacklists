import discord
from discord import app_commands
from discord.ext import commands
from utils.checks import is_admin_team
from utils.database import blacklist_user, unblacklist_user
from utils.logging import log_blacklist_action

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="blacklist", description="Blacklist a user across all shared servers.")
    @is_admin_team()
    async def blacklist(self, interaction: discord.Interaction, user: discord.User, reason: str, additional_info: str = None):
        # Ban user from all servers except the appeals server
        banned_servers = []
        for guild in self.bot.guilds:
            if guild.id != 1236376514430500914:  # Exclude the appeals server
                try:
                    await guild.ban(user, reason=reason)
                    banned_servers.append(guild.name)
                except discord.Forbidden:
                    pass

        # Save blacklist data in MongoDB
        blacklist_user(user.id, reason, interaction.user.id, banned_servers)

        # Create the embed for confirmation
        embed = discord.Embed(
            title="User Blacklisted",
            description=f"{user.mention} has been blacklisted across all shared servers.",
            color=discord.Color(0x013a93)
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Banned Servers", value=", ".join(banned_servers), inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/689530498837381210/1281538937021661254/image.png")
        await interaction.response.send_message(embed=embed)

        # Log the blacklist action in the specified channel
        await log_blacklist_action(self.bot, user, reason, additional_info, interaction.user, banned_servers)

    @app_commands.command(name="unblacklist", description="Unblacklist a user.")
    @is_admin_team()
    async def unblacklist(self, interaction: discord.Interaction, user: discord.User):
        # Unban user from all servers
        for guild in self.bot.guilds:
            try:
                await guild.unban(user)
            except discord.NotFound:
                pass

        # Remove blacklist entry from MongoDB
        unblacklist_user(user.id)

        # Create the embed for confirmation
        embed = discord.Embed(
            title="User Unblacklisted",
            description=f"{user.mention} has been unblacklisted from all servers.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/689530498837381210/1281538937021661254/image.png")
        await interaction.response.send_message(embed=embed)

        # Log the unblacklist action in the specified channel
        await log_blacklist_action(self.bot, user, "Unblacklisted", None, interaction.user, [])

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
