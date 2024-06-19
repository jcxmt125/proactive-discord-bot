import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", description="a bot that will respond to you", intents=intents)
@bot.event
async def on_message(ctx):
    print(ctx)
    if ctx.author == bot.user:
        return

    if ctx.content.startswith('$hello'):
        await ctx.channel.send('Hello!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(os.getenv("DISCORD_BOT_TOKEN"))