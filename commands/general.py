import discord
from discord import app_commands
from discord.ext import commands

# Command IDs organized
COMMAND_IDS = {
    "blacklist": "1293544631858102383",
    "unblacklist": "1293544631858102384",
    "ban-user": "1293580200172458125",
    "unban-user": "1293580200172458126",
    "invite-link": "1293580200172458127",
    "check-status": "1293580200172458122",
    "lookup-user": "1293580200172458123",
    "edit-reason": "1293580200172458124",
    "eval": "1293544631858102385",
    "sudo": "1293544631858102386",
    "reload": "1293552354481803350",
    "kick-user": "1293580200172458128",
    "say": "1293585487239581707",
    "embed-say": "1293585487239581708",
    "help": "1293594584840011828",
}

# Define or import the role IDs at the top of your file
MOD_TEAM_1 = 1236358475827904664  # Replace with actual ID
MOD_TEAM_2 = 1236379144141541489  # Replace with actual ID
ADMIN_TEAM_1 = 1225934070794555455  # Replace with actual ID
ADMIN_TEAM_2 = 1236379225565433927  # Replace with actual ID
DEV_USER_ID = 186117507554344960  # Bot developer's user ID

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
            "Administration Team Commands": [
                {
                    "name": f"</blacklist:{COMMAND_IDS['blacklist']}>",
                    "description": "Blacklist a user across all shared servers."
                },
                {
                    "name": f"</unblacklist:{COMMAND_IDS['unblacklist']}>",
                    "description": "Unblacklist a user."
                },
                {
                    "name": f"</ban-user:{COMMAND_IDS['ban-user']}>",
                    "description": "Ban a user from a specific server."
                },
                {
                    "name": f"</unban-user:{COMMAND_IDS['unban-user']}>",
                    "description": "Unban a user from a specific server."
                },
                {
                    "name": f"</invite-link:{COMMAND_IDS['invite-link']}>",
                    "description": "Create an invite link for a server."
                },
            ],
            "Moderation Team Commands": [
                {
                    "name": f"</check-status:{COMMAND_IDS['check-status']}>",
                    "description": "Check if a user is blacklisted."
                },
                {
                    "name": f"</lookup-user:{COMMAND_IDS['lookup-user']}>",
                    "description": "Lookup a user and show their roles in shared servers."
                },
                {
                    "name": f"</edit-reason:{COMMAND_IDS['edit-reason']}>",
                    "description": "Edit the reason for a blacklist case."
                },
            ],
            "Bot Developer Commands": [
                {
                    "name": f"</eval:{COMMAND_IDS['eval']}>",
                    "description": "Evaluate Python code."
                },
                {
                    "name": f"</sudo:{COMMAND_IDS['sudo']}>",
                    "description": "Execute commands as another user."
                },
                {
                    "name": f"</reload:{COMMAND_IDS['reload']}>",
                    "description": "Reloads the bot for maintenance or updates."
                },
                {
                    "name": f"</kick-user:{COMMAND_IDS['kick-user']}>",
                    "description": "Kick a user from all servers (excluding appeals server)."
                },
                {
                    "name": f"</say:{COMMAND_IDS['say']}>",
                    "description": "Make the bot say something in a specified channel."
                },
                {
                    "name": f"</embed-say:{COMMAND_IDS['embed-say']}>",
                    "description": "Make the bot say something in an embed format."
                },
            ],
        }

        # Check user's roles and add relevant commands to the embed
        user_roles = [role.id for role in interaction.user.roles]  # Get user roles

        if any(role in [MOD_TEAM_1, MOD_TEAM_2, DEV_USER_ID] for role in user_roles):
            embed.add_field(
                name="Moderation Team Commands",
                value="\n".join(
                    [f"{cmd['name']} - {cmd['description']}" for cmd in commands_list["Moderation Team Commands"]]
                ),
                inline=False
            )

        if any(role in [ADMIN_TEAM_1, ADMIN_TEAM_2, DEV_USER_ID] for role in user_roles):
            embed.add_field(
                name="Administration Team Commands",
                value="\n".join(
                    [f"{cmd['name']} - {cmd['description']}" for cmd in commands_list["Administration Team Commands"]]
                ),
                inline=False
            )

        if interaction.user.id == DEV_USER_ID:  # Check if the user is a bot developer
            embed.add_field(
                name="Bot Developer Commands",
                value="\n".join(
                    [f"{cmd['name']} - {cmd['description']}" for cmd in commands_list["Bot Developer Commands"]]
                ),
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))