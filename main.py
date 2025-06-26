import discord
from aiohttp.helpers import DEBUG
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token=os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

server_role = "TestRole"

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Hello {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} wrong word used")

    await bot.process_commands(message)


@bot.command()
async def hey(ctx):
    await ctx.send(f"Hey {ctx.author.mention}")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=server_role)

    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} You are now assigned to {role}")
    else:
        await ctx.send("role doesnt exist")

@bot.command()
async def unassign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=server_role)

    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has the {role} removed from {ctx.guild.name}")
    else:
        await ctx.send("role doesnt exist")

@bot.command()
@commands.has_role(server_role)
async def main_role(ctx):
    await ctx.send(f"Yes has it")

@main_role.error
async def main_role_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"You don't have the {server_role} role")

@bot.command()
async def dm(ctx,*,msg):
    await ctx.author.send(msg)

@bot.command()
async def reply(ctx):
    await ctx.reply("This is the reply")

@bot.command()
async def poll(ctx,*, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("🅾️")
    await poll_message.add_reaction("❌")







bot.run(token, log_handler=handler, log_level=logging.DEBUG)



