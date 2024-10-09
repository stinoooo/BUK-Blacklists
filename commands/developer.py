import discord
from discord.ext import commands
from discord import app_commands
from utils.checks import is_bot_developer
import os
import sys  # Ensure sys is imported for the reload functionality

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="eval", description="Evaluate Python code.")
    @is_bot_developer()
    async def eval(self, interaction: discord.Interaction, code: str):
        try:
            result = eval(code)
            embed = discord.Embed(
                title="Evaluation Result",
                description=f"Result: {result}",
                color=discord.Color(0x013a93)
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred: {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="sudo", description="Execute commands as another user.")
    @is_bot_developer()
    async def sudo(self, interaction: discord.Interaction, user: discord.User, command: str):
        # Attempt to find the command by name
        cmd = self.bot.get_command(command)
        if cmd is None:
            await interaction.response.send_message("Command not found.", ephemeral=True)
            return
        
        # Create a fake context for the command
        fake_ctx = await self.bot.get_context(interaction)
        fake_ctx.author = user
        
        try:
            await cmd.invoke(fake_ctx)  # Call the command using the fake context
            await interaction.response.send_message(f"Executed command '{command}' as {user.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to execute command: {e}", ephemeral=True)

    @app_commands.command(name="reload", description="Reloads the bot for maintenance or updates.")
    @is_bot_developer()
    async def reload_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Reloading Bot",
            description="The bot is reloading, please wait...",
            color=discord.Color(0x013a93)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        os.execv(sys.executable, ['python'] + sys.argv)

    @app_commands.command(name="kick-user", description="Kick a user from all servers (excluding appeals server).")
    @is_bot_developer()
    async def kick_user(self, interaction: discord.Interaction, user: discord.User):
        kicked_servers = []
        for guild in self.bot.guilds:
            if guild.id != 1236376514430500914:  # Exclude the appeals server
                try:
                    await guild.kick(user)
                    kicked_servers.append(guild.name)
                except discord.Forbidden:
                    continue
        
        embed = discord.Embed(
            title="Kick User",
            description=f"User {user.mention} has been kicked from the following servers:",
            color=discord.Color(0x013a93)
        )
        if kicked_servers:
            embed.add_field(name="Kicked From", value=", ".join(kicked_servers), inline=False)
        else:
            embed.add_field(name="Error", value="User could not be kicked from any server.", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="say", description="Make the bot say something in a specified channel.")
    @is_bot_developer()
    async def say(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
        if channel is None:
            channel = interaction.channel  # Use current channel if none specified

        await channel.send(message)
        embed = discord.Embed(
            title="Message Sent",
            description=f"Message has been sent to {channel.mention}.",
            color=discord.Color(0x013a93)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="embed-say", description="Make the bot say something in an embed format.")
    @is_bot_developer()
    async def embed_say(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
        if channel is None:
            channel = interaction.channel  # Use current channel if none specified

        embed = discord.Embed(
            description=message,
            color=0x013a93  # Standard color for embeds
        )
        await channel.send(embed=embed)
        embed_response = discord.Embed(
            title="Embed Sent",
            description=f"Embed has been sent to {channel.mention}.",
            color=discord.Color(0x013a93)
        )
        await interaction.response.send_message(embed=embed_response, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Developer(bot))