import discord
from discord.ext import commands
from discord import app_commands
from utils.checks import is_bot_developer

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="eval", description="Evaluate Python code.")
    @is_bot_developer()
    async def eval(self, interaction: discord.Interaction, code: str):
        try:
            result = eval(code)
            await interaction.response.send_message(f"Result: {result}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="sudo", description="Execute commands as another user.")
    @is_bot_developer()
    async def sudo(self, interaction: discord.Interaction, user: discord.User, command: str):
        fake_ctx = await self.bot.get_context(interaction)
        fake_ctx.author = user
        await self.bot.process_commands(fake_ctx)

    @app_commands.command(name="reload", description="Reloads the bot for maintenance or updates.")
    @is_bot_developer()
    async def reload_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Reloading bot...", ephemeral=True)
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
                    pass
        await interaction.response.send_message(f"User {user.mention} kicked from: {', '.join(kicked_servers)}", ephemeral=True)

    @app_commands.command(name="say", description="Make the bot say something in a specified channel.")
    @is_bot_developer()
    async def say(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
        # Delete the original command message
        await interaction.delete_original_response()

        if channel is None:
            channel = interaction.channel  # Use current channel if none specified

        await channel.send(message)

    @app_commands.command(name="embed-say", description="Make the bot say something in an embed format.")
    @is_bot_developer()
    async def embed_say(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
        # Delete the original command message
        await interaction.delete_original_response()

        if channel is None:
            channel = interaction.channel  # Use current channel if none specified

        embed = discord.Embed(
            description=message,
            color=0x013a93  # Standard color for embeds
        )
        await channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Developer(bot))