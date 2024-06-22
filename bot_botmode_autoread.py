import discord, requests
from discord.ext import commands
import os
from dotenv import load_dotenv
import nltocommand
from geminillm import gemrequest
import json
from urlextract import URLExtract
from cfradar import urlScan
from cfsd import sdgen
import cfllm
from pathlib import Path
from htmlify import makePage
from UploadFile import uploadFileToCloud
import localconverters, subprocess

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", description="a bot that will respond to you", intents=intents)

#load settings from JSON file (it should only use except when running for the first time)
#guild:channelid = respond only in a channel
#guild:channelid+- = non-hardcode response only in channel, hardcode response everywhere
try:
    with open('data/channels.json') as f:
        channeldatainit = json.load(f)
except:
    with open('data/channels.json', 'w') as f:
        json.dump({"guild": "channelid"}, f)
    with open('data/channels.json') as f:
        channeldatainit = json.load(f)

#TODO make this able to handle multiple requests
@bot.event
async def on_message(ctx):
    #Variables to adjust
    #Longer context length seems to cause issues. Let's try 1... (for some commands I might indiviudally make it longer)
    contextLength = 1
    listOfActions = ["0. Factual responses", "1. URL scanning" "2. Image generation", "3. Media download"]

    channels = channeldatainit


    #single channel mmode setup
    if ctx.content.startswith('$setup'):

        channels[str(ctx.guild.id)] = str(ctx.channel.id)

        with open('data/channels.json', 'w') as f:
            json.dump(channels, f)

        with open('data/channels.json') as f:
            channels = json.load(f)

        await ctx.channel.send("Okay, I'll only reply in this channel!")

        return
    
    elif ctx.content.startswith('$verbosesetup'):

        channels[str(ctx.guild.id)] = str(ctx.channel.id)+"-"

        with open('data/channels.json', 'w') as f:
            json.dump(channels, f)

        with open('data/channels.json') as f:
            channels = json.load(f)

        await ctx.channel.send("Okay, I'll only do AI responses in this channel! Harcoded responses will run everywhere.")

        return

    if ctx.author == bot.user:
        return

    correctChannel = False
    verboseMode = False

    if (str(ctx.channel.id) == channels[str(ctx.guild.id)][0:-1]) or (str(ctx.channel.id) == channels[str(ctx.guild.id)]):
        correctChannel = True

    if channels[str(ctx.guild.id)][-1] == "-":
        verboseMode = True

    #hardcode
    if correctChannel or verboseMode:
        attachments = ctx.attachments
        #attachment related hardcoding
        #AVIF/HEIF conversion, txt file handling, opus file conversion
        if len(attachments) != 0:
            
            listoldfiles = []
            listnewfiles = []
            listnewfilenames = []
            listnewlinks = []
                
            for i in attachments:

                ctype = i.content_type.split('/')
                filename = i.filename
                
                if ctype[0] == "image":
                    if ctype[1] == "heic" or ctype[1] == "avif":
                        await i.save(fp=filename)

                        listoldfiles.append(filename)

                        localconverters.imagemagick(filename,"webp")
                        
                        splitname = filename.split(".")

                        noext = ""

                        for i in range(len(splitname)-1):
                            noext += splitname[i]

                        newfilename = noext+".webp"

                        print(newfilename)

                        listnewfiles.append(discord.File(newfilename))
                        listnewfilenames.append(newfilename)
                
                elif ctype[0] == "text":
                    await i.save(fp=filename)

                    listoldfiles.append(filename)
                    
                    with open(filename, "r", encoding="UTF-8") as txtfile:
                        htmlLoc = makePage(txtfile.readlines(), description="Automatically generated page from "+filename)
                    
                    link = uploadFileToCloud(htmlLoc, "webpage/")
                    
                    listnewfilenames.append(htmlLoc)

                    listnewlinks.append(link)

                elif ctype[0] == "audio":
                    if ctype[1] == "opus":
                        await i.save(fp=filename)

                        listoldfiles.append(filename)

                        localconverters.ffmpeg(filename,"mp3")
                        
                        splitname = filename.split(".")

                        noext = ""

                        for i in range(len(splitname)-1):
                            noext += splitname[i]

                        newfilename = noext+".mp3"

                        print(newfilename)

                        listnewfiles.append(discord.File(newfilename))
                        listnewfilenames.append(newfilename)
                    

            if len(listnewfiles) != 0 or len(listnewlinks) != 0:
                
                message = ""

                for i in listnewlinks:
                    message += i
                    message += "\n"
                
                await ctx.channel.send(message, files=listnewfiles)

                #Clean up the downloaded files
                for i in listoldfiles:
                    Path.unlink(Path(i))
                for j in listnewfilenames:
                    Path.unlink(Path(j))

                    return
                
            

                        
    #AI responses

    if not correctChannel:
        return

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

            elif interpreted == 2: #Image generation
                #We'll first want to turn the text into a usable prompt.
                #I think we all know where this is going...

                construct = "Create a usable Stable Diffusion prompt from the following messages.\n"
                for i in messagesPlaintextList:
                    construct += i
                    construct += "\n"

                #I am very unsure how well this will work
                #Update on that: it took... so many... tries... to get the prompt right-
                prompt = cfllm.nsllmreq("You are a creative assistant that follows messgaes exactly. Only reply with the prompt.",construct)

                sdgen(prompt)

                await ctx.channel.send("Prompt: "+prompt,file=discord.File('output.png'))

                Path.unlink(Path("output.png"))
            
            elif interpreted == 3:#media download aka yt-dlp
                url = URLExtract().find_urls(messagesPlaintextList[-1])[0]
                
                subprocess.run(["yt-dlp","-x","-o","video",url])

                localconverters.ffmpeg("video.opus","mp3")

                await ctx.channel.send(file=discord.File("video.mp3"))

                Path.unlink(Path("video.opus"))
                Path.unlink(Path("video.mp3"))

    else:
        return


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(os.getenv("DISCORD_BOT_TOKEN"))