import discord
from discord import app_commands
from discord.ext import commands
from utils.checks import is_admin_team
from utils.database import blacklist_user, unblacklist_user
from utils.logging import log_blacklist_action
import random  # For generating case IDs

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="blacklist", description="Blacklist a user across all shared servers.")
    @is_admin_team()
    async def blacklist(self, interaction: discord.Interaction, user: discord.User, reason: str):
        banned_servers = []
        case_id = random.randint(10000, 99999)  # Generate a unique case ID
        for guild in self.bot.guilds:
            if guild.id != 1236376514430500914:  # Exclude the appeals server
                try:
                    await guild.ban(user, reason=reason)
                    banned_servers.append(guild.name)
                except discord.Forbidden:
                    pass

        # Store the blacklist entry in the database with case ID
        blacklist_user(user.id, reason, interaction.user.id, banned_servers, case_id)
        
        embed = discord.Embed(
            title="User Blacklisted",
            description=f"{user.mention} has been blacklisted across all shared servers.",
            color=discord.Color(0x013a93)
        )
        embed.add_field(name="Case ID", value=case_id, inline=False)  # Show case ID
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Banned Servers", value=", ".join(banned_servers), inline=False)
        await interaction.response.send_message(embed=embed)

        await log_blacklist_action(self.bot, user, reason, None, interaction.user, banned_servers)

    @app_commands.command(name="unblacklist", description="Unblacklist a user.")
    @is_admin_team()
    async def unblacklist(self, interaction: discord.Interaction, user: discord.User):
        for guild in self.bot.guilds:
            try:
                await guild.unban(user)
            except discord.NotFound:
                pass

        unblacklist_user(user.id)

        embed = discord.Embed(
            title="User Unblacklisted",
            description=f"{user.mention} has been unblacklisted from all servers.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

        await log_blacklist_action(self.bot, user, "Unblacklisted", None, interaction.user, [])

    @app_commands.command(name="ban user", description="Ban a user from a specific server.")
    @is_admin_team()
    async def ban_user(self, interaction: discord.Interaction, user: discord.User, reason: str):
        guilds = [guild for guild in self.bot.guilds if user in guild.members]
        
        if not guilds:
            await interaction.response.send_message("User not found in any shared servers.", ephemeral=True)
            return
        
        # Create a dropdown menu to select a server
        options = [
            discord.SelectOption(label=guild.name, value=str(guild.id), description=f"Ban from {guild.name}", emoji=guild.icon.url)
            for guild in guilds
        ]
        
        select = discord.ui.Select(placeholder="Select a server to ban from", options=options)
        
        async def select_callback(interaction: discord.Interaction):
            selected_guild_id = int(select.values[0])
            guild = self.bot.get_guild(selected_guild_id)
            await guild.ban(user, reason=reason)
            embed = discord.Embed(
                title="User Banned",
                description=f"{user.mention} has been banned from {guild.name}.",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            await interaction.response.send_message(embed=embed)
        
        select.callback = select_callback
        view = discord.ui.View()
        view.add_item(select)
        await interaction.response.send_message("Please select a server to ban from:", view=view)

    @app_commands.command(name="unban user", description="Unban a user from a specific server.")
    @is_admin_team()
    async def unban_user(self, interaction: discord.Interaction, user: discord.User):
        guilds = [guild for guild in self.bot.guilds if user not in guild.bans]

        if not guilds:
            await interaction.response.send_message("User not found in any shared servers.", ephemeral=True)
            return

        # Create a dropdown menu to select a server
        options = [
            discord.SelectOption(label=guild.name, value=str(guild.id), description=f"Unban from {guild.name}", emoji=guild.icon.url)
            for guild in guilds
        ]
        
        select = discord.ui.Select(placeholder="Select a server to unban from", options=options)
        
        async def select_callback(interaction: discord.Interaction):
            selected_guild_id = int(select.values[0])
            guild = self.bot.get_guild(selected_guild_id)
            await guild.unban(user)
            embed = discord.Embed(
                title="User Unbanned",
                description=f"{user.mention} has been unbanned from {guild.name}.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        
        select.callback = select_callback
        view = discord.ui.View()
        view.add_item(select)
        await interaction.response.send_message("Please select a server to unban from:", view=view)

    @app_commands.command(name="invite link", description="Create an invite link for a server.")
    @is_admin_team()
    async def invite_link(self, interaction: discord.Interaction):
        # Create a dropdown menu for server selection
        guilds = self.bot.guilds  # Include all servers the bot is in
        options = [discord.SelectOption(label=guild.name, value=str(guild.id)) for guild in guilds]

        select = discord.ui.Select(placeholder="Select a server to create an invite link", options=options)

        async def select_callback(interaction: discord.Interaction):
            selected_guild = self.bot.get_guild(int(select.values[0]))
            invite = await selected_guild.text_channels[0].create_invite(max_age=3600)  # 1-hour invite
            await interaction.response.send_message(f"Invite link for {selected_guild.name}: [Click Here]({invite})", ephemeral=True)

        select.callback = select_callback
        view = discord.ui.View()
        view.add_item(select)

        await interaction.response.send_message("Select a server to create an invite link:", view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))