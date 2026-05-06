import discord
from discord.ext import commands
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "warns.json")

intents = discord.Intents.all()
intents.message_content = True  # allows reading messages

client = commands.Bot(command_prefix='?', intents=intents)

def load_warns():
    if not os.path.exists(JSON_PATH):
        return {}
    with open(JSON_PATH, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_warns(data):
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} and ready to help!")

# warn command
@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="not specified"):
    if member == ctx.author:
        return await ctx.send("You cannot warn yourself...")

warns = load_warns()
    guild_id = str(ctx.guild.id)
    member_id = str(member.id)

    if guild_id not in warns:
        warns[guild_id] = {}
    
    if member_id not in warns[guild_id]:
        warns[guild_id][member_id] = []

    # Add the warning entry
    warn_entry = {
        "reason": reason,
        "warner_id": ctx.author.id,
        "timestamp": str(ctx.message.created_at)
    }
    warns[guild_id][member_id].append(warn_entry)
    
    save_warns(warns)
    total_warns = len(warns[guild_id][member_id])
    
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
