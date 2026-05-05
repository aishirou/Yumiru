import discord
from discord.ext import commands


intents = discord.Intents.all()
intents.message_content = True  # allows reading messages

client = commands.Bot(command_prefix='?', intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} and ready to help!")

# warn command
@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="not specified"):
    if member == ctx.author:
        return await ctx.send("You cannot warn yourself...")
    
    # send to the channel
    en = discord.Embed(
        title="User Warned", 
        description=f"{member.mention} was successfully warned! \n**Reason:** {reason}", 
        color=discord.Color.red()
    )
    
    # send to the user's DMs
    en2 = discord.Embed(
        title="Warning Received", 
        description=f"You were warned in {ctx.guild.name}! \n**Reason:** {reason}", 
        color=discord.Color.red()
    )
    
    try:
        await member.send(embed=en2)
    except discord.Forbidden:
        await ctx.send("I couldn't DM that user, but the warn has been logged.")

    await ctx.send(embed=en)
    
@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Nice try bro, but you don't have permission to warn people.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: `?warn @user [reason]`")

client.run('TOKEN')
