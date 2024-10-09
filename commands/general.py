import discord
from discord import app_commands
from discord.ext import commands

# Define or import the role IDs at the top of your file
MOD_TEAM_1 = 1236358475827904664  # Replace with actual ID
ADMIN_TEAM_1 = 1225934070794555455  # Replace with actual ID
DEV_USER_ID = 186117507554344960  # Bot developer's user ID
MOD_TEAM_2 = 1236379144141541489  # Replace with actual ID
ADMIN_TEAM_2 = 1236379225565433927  # Replace with actual ID

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="List all available commands based on your permissions.")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Help - Available Commands",
            color=discord.Color(0x013a93)
        )

        commands_list = {
            "Admin Commands": [
                {
                    "name": "/blacklist",
                    "description": "Blacklist a user across all shared servers."
                },
                {
                    "name": "/unblacklist",
                    "description": "Unblacklist a user."
                },
                {
                    "name": "/ban-user",
                    "description": "Ban a user from a specific server."
                },
                {
                    "name": "/unban-user",
                    "description": "Unban a user from a specific server."
                },
                {
                    "name": "/invite-link",
                    "description": "Create an invite link for a server."
                },
            ],
            "Moderation Commands": [
                {
                    "name": "/check-status",
                    "description": "Check if a user is blacklisted."
                },
                {
                    "name": "/lookup-user",
                    "description": "Lookup a user and show their roles in shared servers."
                },
                {
                    "name": "/edit-reason",
                    "description": "Edit the reason for a blacklist case."
                },
            ],
            "Bot Developer Commands": [
                {
                    "name": "/eval",
                    "description": "Evaluate Python code."
                },
                {
                    "name": "/sudo",
                    "description": "Execute commands as another user."
                },
                {
                    "name": "/reload",
                    "description": "Reloads the bot for maintenance or updates."
                },
                {
                    "name": "/kick-user",
                    "description": "Kick a user from all servers (excluding appeals server)."
                },
                {
                    "name": "/say",
                    "description": "Make the bot say something in a specified channel."
                },
                {
                    "name": "/embed-say",
                    "description": "Make the bot say something in an embed format."
                },
            ],
        }

        # Check user's roles and add relevant commands to the embed
        if any(role.id in [MOD_TEAM_1, MOD_TEAM_2] for role in interaction.user.roles):
            embed.add_field(
                name="Moderation Commands",
                value="\n".join(
                    [f"[{cmd['name']}]({cmd['name']}) - {cmd['description']}" for cmd in commands_list["Moderation Commands"]]
                ),
                inline=False
            )

        if any(role.id in [ADMIN_TEAM_1, ADMIN_TEAM_2] for role in interaction.user.roles):
            embed.add_field(
                name="Admin Commands",
                value="\n".join(
                    [f"[{cmd['name']}]({cmd['name']}) - {cmd['description']}" for cmd in commands_list["Admin Commands"]]
                ),
                inline=False
            )

        if interaction.user.id == DEV_USER_ID:  # Assuming DEV_USER_ID is defined elsewhere
            embed.add_field(
                name="Bot Developer Commands",
                value="\n".join(
                    [f"[{cmd['name']}]({cmd['name']}) - {cmd['description']}" for cmd in commands_list["Bot Developer Commands"]]
                ),
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))