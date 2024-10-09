import discord
from discord.ext import commands
from discord import app_commands

# Role IDs for both guilds
MOD_TEAM_1 = 1236358475827904664
ADMIN_TEAM_1 = 1225934070794555455

MOD_TEAM_2 = 1236379144141541489
ADMIN_TEAM_2 = 1236379225565433927

DEV_USER_ID = 186117507554344960  # Bot developer's user ID

def is_moderation_team():
    async def predicate(interaction: discord.Interaction):
        if interaction.user.id == DEV_USER_ID:  # Allow bot developer to bypass this check
            return True
        if interaction.guild.id == 1225923654207016961:
            return MOD_TEAM_1 in [role.id for role in interaction.user.roles]
        elif interaction.guild.id == 1236376514430500914:
            return MOD_TEAM_2 in [role.id for role in interaction.user.roles]
        return False
    return app_commands.check(predicate)

def is_admin_team():
    async def predicate(interaction: discord.Interaction):
        if interaction.user.id == DEV_USER_ID:  # Allow bot developer to bypass this check
            return True
        if interaction.guild.id == 1225923654207016961:
            return ADMIN_TEAM_1 in [role.id for role in interaction.user.roles]
        elif interaction.guild.id == 1236376514430500914:
            return ADMIN_TEAM_2 in [role.id for role in interaction.user.roles]
        return False
    return app_commands.check(predicate)

def is_bot_developer():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.id == DEV_USER_ID  # Check if user is the bot developer
    return app_commands.check(predicate)

# New check for moderation or admin team
def is_moderation_or_admin():
    async def predicate(interaction: discord.Interaction):
        if interaction.user.id == DEV_USER_ID:  # Allow bot developer to bypass this check
            return True
        if interaction.guild.id == 1225923654207016961:
            return (MOD_TEAM_1 in [role.id for role in interaction.user.roles] or 
                    ADMIN_TEAM_1 in [role.id for role in interaction.user.roles])
        elif interaction.guild.id == 1236376514430500914:
            return (MOD_TEAM_2 in [role.id for role in interaction.user.roles] or 
                    ADMIN_TEAM_2 in [role.id for role in interaction.user.roles])
        return False
    return app_commands.check(predicate)