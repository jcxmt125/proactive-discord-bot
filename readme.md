# Discord bot that responds to you proactively
This is a very work-in-progress project.
The goals are to:
- Make a bot that will respond to you when necessary (Kinda done!)
- Remember who you are (Paused)
- Possibly some tools when required? (WIP)
- Make this bot runnable in... *very* resource constrained (aka GCloud e2-micro) environments. (Seems to work)

To achieve this, we'll likely have to make the bot read every message it gets and figure out when best to respond...
LLMs will likely be used for all decision making.
The last part might create some OS headaches... let's see where this takes us!

By the way, watch for egress when deploying this on a server... especially free tier.

You could also just use the... various python files for other purposes. Just make sure to install dependancies!

## milestone at 24/06/19
This bot will now probably work when deployed!
Run $setup on a channel and try asking some questions.
You will need a .env file though, with the following things:
- CLOUDFLARE_AI_API_KEY, CLOUDFLARE_AI_GATEWAY_SLUG, CLOUDFLARE_USER_ID, CLOUDFLARE_RADAR_API_KEY: Make a cloudflare account, and make the API keys. You might have to set up billing... Don't worry, none of these will charge for usage unless you sign up for paid plans.
- S3COMPAT_ENDPOINT_URL, S3KEYID, S3SECRET, S3_BUCKET_PUBLIC_URL, S3_BUCKET_NAME: Sign up for an S3 compatible storage provider of your choice! 
- GEMINI_API_KEY: Get one at google AI studio as detailed above. This is also free as long as you don't set billing up.
- DISCORD_BOT_TOKEN: Get it at Discord Developer portal!

## milestone at 24/06/22

Now with many more functions! You'll need the following external dependancies (non-python):
- ImageMagick (in PATH) (either as magick mogirfy or convert)
- ffmpeg (in PATH)

## updates at 24/06/23

Now with advanced settings! (Documentation and bugfixes ongoing)
HelpEverywhere ImageConversion AudioConversion TextPublish EmojiMagnify AIEnabled AIWebScan AIMediaLoad AIResponse AIImagen

## How are the external tools going?
- Factual responses (straight LLM) (Done!)
- URL scanning (Cloudflare Radar) (Done!)
- Stable Diffusion (CLoudflare AI) (Done!)
- Convert txt file to webpage (Done!)
- Transcribe message (WIP) -> Maybe respond if required? (If voice is a command)
- Convert filetypes? (HEIC/AVIF breaks for discord...) (Done!)