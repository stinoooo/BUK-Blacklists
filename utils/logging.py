import discord

# The modlog channel in guild ID 1225923654207016961 where logs are sent
MODLOG_CHANNEL_ID = 1258619384625365012

async def log_blacklist_action(bot, user, reason, additional_info, admin_user, banned_servers):
    """Logs blacklist and unblacklist actions to the modlog channel."""
    guild = discord.utils.get(bot.guilds, id=1225923654207016961)
    if guild:
        modlog_channel = guild.get_channel(MODLOG_CHANNEL_ID)
        if modlog_channel:
            # Create the embed for logging
            embed = discord.Embed(
                title="Blacklist Action Logged",
                description=f"Action taken on {user.mention}",
                color=discord.Color(0x013a93)
            )
            embed.add_field(name="Action", value="Blacklisted" if banned_servers else "Unblacklisted", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            if additional_info:
                embed.add_field(name="Additional Info", value=additional_info, inline=False)
            embed.add_field(name="Admin", value=f"<@{admin_user.id}>", inline=False)
            if banned_servers:
                embed.add_field(name="Banned Servers", value=", ".join(banned_servers), inline=False)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/689530498837381210/1281538937021661254/image.png")
            embed.set_image(url="https://media.discordapp.net/attachments/689530498837381210/1286019232592826379/CF466648-C77B-4964-A5A8-BECEB8019DC1.jpg")

            # Send the embed to the modlog channel
            await modlog_channel.send(embed=embed)