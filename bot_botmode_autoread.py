#actual python modules
import discord, os, json, subprocess
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

#my own python files
from geminillm import gemrequest
from urlextract import URLExtract
from cfradar import urlScan
from cfsd import sdgen
from htmlify import makePage
from UploadFile import uploadFileToCloud
import localconverters, nltocommand, cfllm, whispercf

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", description="a bot that will respond to you", intents=intents)

#load settings from JSON file (it should only use "except" when running for the first time)
try:
    with open('data/settings.json') as f:
        AllSettings = json.load(f)
    
    #automatically fix compatibility issues with very old setting file
    if AllSettings["guild"] == "settings":
        AllSettings["guild"] = {"settings":True}
        with open('data/settings.json', 'w') as f:
            json.dump(AllSettings, f, indent=2)
        with open('data/settings.json') as f:
            AllSettings = json.load(f)
except:
    #Try to create a new settings file
    try:
        with open('data/settings.json', 'w') as f:
            json.dump({"guild": {"settings":True}}, f, indent=2)
        with open('data/settings.json') as f:
            AllSettings = json.load(f)
    #If even the /data directory doesn't exist
    except:
        os.mkdir("data")
        with open('data/settings.json', 'w') as f:
            json.dump({"guild": {"settings":True}}, f, indent=2)
        with open('data/settings.json') as f:
            AllSettings = json.load(f)

featuresList = ["HelpEverywhere","ImageConversion","AudioConversion","APNGConversion","TextPublish","AIEnabled","AIWebScan","AIMediaLoad","AIResponse","AIImagen","AIAudioTranscribe"]

#auto-migrate
for i in AllSettings:
    for j in featuresList:
        if j not in AllSettings[i]:
            AllSettings[i][j] = False
            with open('data/settings.json', 'w') as f:
                json.dump(AllSettings, f, indent=2)
            with open('data/settings.json') as f:
                AllSettings = json.load(f)

#TODO make this able to handle multiple requests
@bot.event
async def on_message(ctx):
    

    channels = AllSettings

    if ctx.author == bot.user:
        return

    #auto-init (silent)
    if not ctx.guild.id in AllSettings:
        channels[str(ctx.guild.id)] = {
            "MainChannel":ctx.channel.id
        }

        for i in featuresList:
            channels[str(ctx.guild.id)][i] = False

        with open('data/settings.json', 'w') as f:
            json.dump(channels, f, indent=2)

        with open('data/settings.json') as f:
            channels = json.load(f)

    if ctx.content.startswith('$help'):
        await ctx.channel.send("This bot will help you in various tasks!\n\
Basic/Hardcode will always run in your set up channel. Enable `HelpEverywhere` to allow bot to respond everywhere.\n\
List of features: HelpEverywhere ImageConversion AudioConversion APNGConversion TextPublish\n\
AI mode will only run if AIEnabled is on, on the channel the bot saw the first message at by default. Change this with $initialize or $setmainchannel.\n\
List of features: AIWebScan AIMediaLoad AIResponse AIImagen AIAudioTranscribe")
        return
    
    #Change main channel
    elif ctx.content.startswith('$setmainchannel') or ctx.content.startswith('$initialize'):

        try:
            channels[str(ctx.guild.id)]["MainChannel"] = ctx.channel.id

            with open('data/settings.json', 'w') as f:
                json.dump(channels, f, indent=2)

            with open('data/settings.json') as f:
                channels = json.load(f)

            await ctx.channel.send("This channel set as main!")
            return

        except:
            await ctx.channel.send("Something went wrong! Please contact the developer.")
            return

    #Enable features
    elif ctx.content.startswith('$enable'):

        try:
            
            parameters = ctx.content.split()
            
            if len(parameters) == 1:
                await ctx.channel.send("I need a parameter to adjust!")
                return
            
            elif len(parameters) == 2:
                if parameters[1] == "all":
                    for i in featuresList:
                        channels[str(ctx.guild.id)][i] = True
                    with open('data/settings.json', 'w') as f:
                        json.dump(channels, f, indent=2)

                    with open('data/settings.json') as f:
                        channels = json.load(f)

                    await ctx.channel.send("All features enabled!")
                    return
                elif parameters[1] == "AI":
                    for i in featuresList:
                        if i[0:2] == "AI":
                            channels[str(ctx.guild.id)][i] = True

                    with open('data/settings.json', 'w') as f:
                        json.dump(channels, f, indent=2)

                    with open('data/settings.json') as f:
                        channels = json.load(f)

                    await ctx.channel.send("All AI features enabled!")
                    return
                elif parameters[2] == "proactive":
                    for i in featuresList:
                        if i[0:2] != "AI":
                            channels[str(ctx.guild.id)][i] = True

                    with open('data/settings.json', 'w') as f:
                        json.dump(channels, f, indent=2)

                    with open('data/settings.json') as f:
                        channels = json.load(f)

                    await ctx.channel.send("All proactive features enabled!")
                    return

            del(parameters[0])
            
            toSend = ""

            for i in parameters:
                try:
                    if channels[str(ctx.guild.id)][i]:
                        toSend += (i +" is already enabled!\n")
                    else:
                        channels[str(ctx.guild.id)][i] = True
                        toSend += i +" enabled!\n"
                except:
                    toSend += ("Invalid parameter: "+ i +"!\n")
            
            with open('data/settings.json', 'w') as f:
                json.dump(channels, f, indent=2)

            with open('data/settings.json') as f:
                channels = json.load(f)

            await ctx.channel.send(toSend)

            return

        except:
            await ctx.channel.send("Something went wrong! Please contact the developer.")
            return
        
    #Disable features
    elif ctx.content.startswith('$disable'):

        try:
            
            parameters = ctx.content.split()
            
            if len(parameters) == 1:
                await ctx.channel.send("I need a parameter to adjust!")
                return
            
            elif len(parameters) == 2:
                if parameters[1] == "all":
                    for i in featuresList:
                        channels[str(ctx.guild.id)][i] = False
                    with open('data/settings.json', 'w') as f:
                        json.dump(channels, f, indent=2)

                    with open('data/settings.json') as f:
                        channels = json.load(f)

                    await ctx.channel.send("All features enabled!")
                    return
                elif parameters[1] == "AI":
                    for i in featuresList:
                        if i[0:2] == "AI":
                            channels[str(ctx.guild.id)][i] = False

                    with open('data/settings.json', 'w') as f:
                        json.dump(channels, f, indent=2)

                    with open('data/settings.json') as f:
                        channels = json.load(f)

                    await ctx.channel.send("All AI features enabled!")
                    return
                elif parameters[2] == "proactive":
                    for i in featuresList:
                        if i[0:2] != "AI":
                            channels[str(ctx.guild.id)][i] = False

                    with open('data/settings.json', 'w') as f:
                        json.dump(channels, f, indent=2)

                    with open('data/settings.json') as f:
                        channels = json.load(f)

                    await ctx.channel.send("All proactive features enabled!")
                    return
            
            del(parameters[0])
            
            toSend = ""

            for i in parameters:
                try:
                    if not channels[str(ctx.guild.id)][i]:
                        toSend += (i +" is already disabled!\n")
                    else:
                        channels[str(ctx.guild.id)][i] = False
                        toSend += i +" disabled!\n"
                except:
                    toSend += ("Invalid parameter: "+ i +"!\n")
            
            with open('data/settings.json', 'w') as f:
                json.dump(channels, f, indent=2)

            with open('data/settings.json') as f:
                channels = json.load(f)

            await ctx.channel.send(toSend)
            
            return

        except:
            await ctx.channel.send("Something went wrong! Please contact the developer.")
            return

    elif ctx.content.startswith('$listsettings'):
        
        construct = ""
        
        for i in channels[str(ctx.guild.id)]:
            construct += (i +": "+ str(channels[str(ctx.guild.id)][i])+"\n")

        await ctx.channel.send(construct)

        return
    
    elif ctx.content.startswith('$ping'):

        await ctx.channel.send("Running at "+str(round(bot.latency * 1000))+" ms!")

        return
    
    elif ctx.content.startswith("$rickroll"):

        await ctx.channel.send("https://random.jclink.link/serve-rickroll")

        return

    correctChannel = False
    verboseMode = False

    
    listOfActions = []
    
    if channels[str(ctx.guild.id)]["AIResponse"]:
        listOfActions.append("0. Factual responses")

    if channels[str(ctx.guild.id)]["AIWebScan"]:
        listOfActions.append("1. URL scanning")

    if channels[str(ctx.guild.id)]["AIImagen"]:
        listOfActions.append("2. Image generation")
    
    if channels[str(ctx.guild.id)]["AIMediaLoad"]:
        listOfActions.append("3. Media download")

    if channels[str(ctx.guild.id)]["AIAudioTranscribe"]:
        listOfActions.append("4. Audio Transcription")

    if (str(ctx.channel.id) == str(channels[str(ctx.guild.id)]["MainChannel"])):
        correctChannel = True

    if channels[str(ctx.guild.id)]["HelpEverywhere"]:
        verboseMode = True

    #hardcode
    if correctChannel or verboseMode:
        attachments = ctx.attachments
        #attachment related hardcoding
        #AVIF/HEIF/APNG conversion, txt file handling, opus file conversion
        if len(attachments) != 0:
            
            listoldfiles = []
            listnewfiles = []
            listnewfilenames = []
            listnewlinks = []
                
            for i in attachments:

                ctype = i.content_type.split('/')
                filename = i.filename
                
                if ctype[0] == "image" and channels[str(ctx.guild.id)]["ImageConversion"]:
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
                
                elif ctype[0] == "text" and channels[str(ctx.guild.id)]["TextPublish"]:
                    await i.save(fp=filename)

                    listoldfiles.append(filename)
                    
                    with open(filename, "r", encoding="UTF-8") as txtfile:
                        htmlLoc = makePage(txtfile.readlines(), description="Automatically generated page from "+filename)
                    
                    link = uploadFileToCloud(htmlLoc, "webpage/")
                    
                    listnewfilenames.append(htmlLoc)

                    listnewlinks.append(link)

                elif ctype[0] == "audio" and channels[str(ctx.guild.id)]["AudioConversion"]:
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
                
                if ctype[0] == "image" and channels[str(ctx.guild.id)]["APNGConversion"]:
                    if ctype[1] == "vnd.mozilla.apng":
                        await i.save(fp=filename)

                        listoldfiles.append(filename)

                        localconverters.ffmpeg(filename,"webm")
                        
                        splitname = filename.split(".")

                        noext = ""

                        for i in range(len(splitname)-1):
                            noext += splitname[i]

                        newfilename = noext+".webm"

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
                

    #AI context for figuring out what to do
    contextLength = 1

    attachmentSearchContextlength = 5

    extendedContextLength = 3

    #AI responses

    if not (correctChannel and channels[str(ctx.guild.id)]["AIEnabled"]):
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
                urlList = URLExtract().find_urls(messagesPlaintextList[-1])

                if len(urlList) == 0:
                    await ctx.send("I'll try to parse through a few previous messages to find what URL you want scanned...")
                    channel = ctx.channel
                    try:
                        messages = [message async for message in channel.history(limit=attachmentSearchContextlength)]
                    except discord.HTTPException as e:
                        await ctx.send(f"An error occurred: {e}")
                        return
                    
                    messagesPlaintextList = [str(message.author) + ": " + message.content for message in messages]

                    messagesPlaintextList.reverse()

                    urlList.append(URLExtract().find_urls(messagesPlaintextList[-1]))

                url = urlList[0]

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
            
            elif interpreted == 4:#Transcribe with Whisper

                attachments = ctx.message.attachments

                if len(attachments) == 0:
                    await ctx.send("I'll try to parse through a few previous messages to find what file you want transcribed...")
                    channel = ctx.channel
                    try:
                        messages = [message async for message in channel.history(limit=attachmentSearchContextlength)]
                    except discord.HTTPException as e:
                        await ctx.send(f"An error occurred: {e}")
                        return

                    for message in messages:
                        if len(message.attachments) != 0:
                            attachments = message.attachments
                            break
                    
                    if len(attachments) == 0:
                        await ctx.send("I was unable to find an audio file to transcribe. Please try again.")
                        return
                        
                for i in attachments:
                    try:
                        if not (str(i.content_type).split("/")[0] == "audio" ):
                            continue
                        await ctx.send("> " + whispercf.cfwhisper(i.url)["result"]["text"])
                    except:
                        await ctx.send("Sorry, something went wrong while trying to transcribe the file.")

        return

    else:
        return


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(os.getenv("DISCORD_BOT_TOKEN"))