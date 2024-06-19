import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import nltocommand
from geminillm import gemrequest
import json
from urlextract import URLExtract
from cfradar import urlScan

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
    listOfActions = ["0. Factual responses", "1. URL scanning"]

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

    resp = nltocommand.shouldIRespond(listOfActions, messagesPlaintextList)

    print(resp)

    if resp >= 0:#Respond!
        async with ctx.channel.typing():

            #So now we have to figure out what to do...
            interpreted = resp

            print(interpreted)

            if interpreted == 0: #Factual
                construct = "The following are some recent messages. Generate a response most fitting to continue the conversation. Do not act as if you were a user. \n"
                
                for i in messagesPlaintextList:
                    construct += i
                    construct += "\n"

                    await ctx.channel.send(gemrequest(construct)[1])

            elif interpreted == 1: #URL scan (the rate limit is pretty low with this API, probably should only scan the last message sent.)
                url = URLExtract().find_urls(messagesPlaintextList[-1])[0]
                if url[-1] == "/":
                    url = url[0:-1]
                print(url)
                scanResults = urlScan(url)
                try:
                    verdict, timeMade = scanResults
                    if verdict["malicious"]:
                        await ctx.channel.send("The URL is likely malicious, catergorized as "+str(verdict["categories"])+". The report was made on "+timeMade+". Do NOT access the webpage for your own safety.")
                    else:
                        await ctx.channel.send("The URL is likely safe. The report was made on "+timeMade+".")
                except:
                    await ctx.channel.send("I've sent a request to scan the URL. The report should be available at https://radar.cloudflare.com/scan/"+scanResults+" in a few minutes. Check here, or run this command again!")

            
    else:
        return


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(os.getenv("DISCORD_BOT_TOKEN"))