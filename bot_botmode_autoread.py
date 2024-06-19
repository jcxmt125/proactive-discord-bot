import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from nltocommand import shouldIRespond, nltocommand
from geminillm import gemrequest
import json

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", description="a bot that will respond to you", intents=intents)

#load settings from JSON file (it should only use except when running for the first time)
try:
    with open('data/channels.json') as f:
        channeldatainit = json.load(f)
except:
    with open('data/channels.json', 'w') as f:
        json.dump({"guild": "channelid"}, f)
    with open('data/channels.json') as f:
        channeldatainit = json.load(f)

@bot.event
async def on_message(ctx):
    #Variables to adjust
    contextLength = 3
    listOfActions = ["0. Factual responses"]

    channels = channeldatainit

    if ctx.content.startswith('$setup'):

        channels[ctx.guild.id] = ctx.channel.id

        with open('data/channels.json', 'w') as f:
            json.dump(channels, f)

        with open('data/channels.json') as f:
            channels = json.load(f)

        await ctx.channel.send("Okay, I'll only reply in this channel!")

        return

    if ctx.author == bot.user:
        return
    
    if ctx.channel.id != channels[str(ctx.guild.id)]:
        return

    print("Correct channel")

    channel = ctx.channel
    try:
        messages = [message async for message in channel.history(limit=contextLength)]
    except discord.HTTPException as e:
        await ctx.channel.send(f"An error occurred: {e}")
        return
    
    messagesPlaintextList = [str(message.author) + ": " + message.content for message in messages]

    messagesPlaintextList.reverse()

    print(messagesPlaintextList)

    resp = shouldIRespond(listOfActions, messagesPlaintextList)

    print(resp)

    if resp == 1:#Respond!
        construct = "The following are some recent messages. Generate a response most fitting to continue the conversation. Do not act as if you were a user. \n"
        
        for i in messagesPlaintextList:
            construct += i
            construct += "\n"

        await ctx.channel.send(gemrequest(construct)[1])
    else:
        return


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(os.getenv("DISCORD_BOT_TOKEN"))