import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from nltocommand import shouldIRespond, nltocommand

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", description="a bot that will respond to you", intents=intents)
@bot.event
async def on_message(ctx):

    #Variables to adjust
    contextLength = 5
    listOfActions = ["0. Factual responses"]

    print(ctx)
    if ctx.author == bot.user:
        return
    
    channel = ctx.channel
    try:
        messages = [message async for message in channel.history(limit=contextLength)]
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {e}")
        return
    
    messagesPlaintextList = [str(message.author) + ": " + message.content for message in messages]
    
    resp = shouldIRespond(listOfActions, messagesPlaintextList)

    print(resp)



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(os.getenv("DISCORD_BOT_TOKEN"))