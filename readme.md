# Discord bot that responds to you proactively
This is a very work-in-progress project.
The goals are to:
- Make a bot that will respond to you when necessary (Kinda done!)
- Remember who you are (Abandoned; will be implemented in a seperate bot)
- Possibly some tools when required? (WIP)
- Make this bot runnable in... *very* resource constrained (aka GCloud e2-micro) environments. (Seems to work)

To achieve this, we'll likely have to make the bot read every message it gets and figure out when best to respond...
LLMs will likely be used for all decision making.
APIs will be used in most cases, local converters in some limited cases (burstable)



By the way, watch for egress when deploying this on a server... especially free tier.

You could also just use the... various python files for other purposes. Just make sure to install dependancies!

## Deploying
First, clone this repository!

Then, make a .env file, with the following things:
- CLOUDFLARE_AI_API_KEY, CLOUDFLARE_AI_GATEWAY_SLUG, CLOUDFLARE_USER_ID, CLOUDFLARE_RADAR_API_KEY: Make a cloudflare account, and make the API keys. You might have to set up billing... Don't worry, none of these will charge for usage unless you sign up for paid plans.
- S3COMPAT_ENDPOINT_URL, S3KEYID, S3SECRET, S3_BUCKET_PUBLIC_URL, S3_BUCKET_NAME: Sign up for an S3 compatible storage provider of your choice! 
- GEMINI_API_KEY: Get one at google AI studio as detailed above. This is also free as long as you don't set billing up.
- DISCORD_BOT_TOKEN: Get it at Discord Developer portal!

Install the following programs:
- ImageMagick (in PATH) (either as magick mogrify or convert)
- ffmpeg (in PATH)

First, $initialize in a channel!
$help for more info about features.
$enable or $disable the ones you want!

## milestone at 24/06/24

Now with settings!
- HelpEverywhere: This will allow the bot to respond with hardcoded responses anywhere. (If off: only in the specified channel)
    - ImageConversion: The bot will auto-convert heic and avif files to webp
    - AudioConversion: The bot will auto-convert opus files to mp3
    - TextPublish: The bot will automatically publish a txt file as a webpage
- AIEnabled: Enables AI scanning in the specified channel to respond with more features. (It won't run anywhere else)
    - AIWebScan: detects, extracts, and scans websites for safety
    - AIMediaLoad: downloads audio tracks from youtube
    - AIResponse: AI responses for factual questions
    - AIImagen: Generates images with Stable Diffusion
    - AIAudioTrancscribe: Transcribes audio when prompted
