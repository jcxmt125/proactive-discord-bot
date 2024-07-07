# Discord bot that responds to you proactively

For web-based documentation, see [here](https://hackclub.jclink.link/documentations/discord-bots/proactive-discord-bot)

## Deploying
First, `git clone` this repository! (or download it)

Then, make a .env file, with the following things:
- `CLOUDFLARE_AI_API_KEY`, `CLOUDFLARE_AI_GATEWAY_SLUG`, `CLOUDFLARE_USER_ID`, `CLOUDFLARE_RADAR_API_KEY`: Make a cloudflare account, and make the API keys. You might have to set up billing... Don't worry, none of these will charge for usage unless you sign up for paid plans.
- `S3COMPAT_ENDPOINT_URL`, `S3KEYID`, `S3SECRET`, `S3_BUCKET_PUBLIC_URL`, `S3_BUCKET_NAME`: Sign up for an S3 compatible storage provider of your choice! For my own use, I'm using cloudflare's R2. Backblaze's B2 also provides some free storage! (We'll only upload small text files here for now, to the /webpage/ prefix.)
- `GEMINI_API_KEY`: Get one at [google AI studio](https://aistudio.google.com) as detailed above. This is also free as long as you don't set billing up. The code is currently set to use the `gemini-flash-1.5-latest` model. Adjust as you please, but other models may be slower or have lower free limits.
- `DISCORD_BOT_TOKEN`: Get it at the Discord Developer portal!

Install the following programs:
- ImageMagick (in PATH, either as `magick mogrify` or `convert`)
- `ffmpeg` (in PATH)

Run the bot's file. This Python file has to be kept running for your bot to function! I recommend getting a spare computer, or if your situation doesn't allow, getting an e2-micro or similar low/no-cost cloud server. This bot is designed to be minimal in terms of resource usage, except for the occasional bursts when converting files. (Resource usage may vary based on what server you use this in)

Invite the bot to your server, and `$initialize` or `$setmainchannel`. (You *may* have to run it twice if your server is inactive, as it needs at least one message to "remember" your server.)
`$help` for more info about features.
`$enable` or `$disable` the ones you want!
`$enable/disable all/AI/proactive` is also supported, as well as multiple settings at once (seperate them with spaces)

To update, simply `git pull`!

### list of settings/features:

- HelpEverywhere: This will allow the bot to respond with hardcoded responses anywhere. (If off: only in the specified channel)
    - ImageConversion: The bot will auto-convert `heic` and `avif` files to `webp` (imagemagick required)
    - AudioConversion: The bot will auto-convert `opus` files to `mp3` (ffmpeg required)
    - TextPublish: The bot will automatically publish a `txt` file as a webpage (uploads to S3-compatible storage)
    - APNGConversion: The bot will auto convert `apng` files to `webm`
- AIEnabled: Enables AI scanning in the specified channel to respond with more features. (It won't run anywhere else)
    - AIWebScan: detects, extracts, and scans websites for safety (uses cloudflare radar only for the most recent link within 5 messages)
    - AIMediaLoad: downloads audio tracks from youtube (uses yt-dlp)
    - AIResponse: AI responses for factual questions (uses Gemini LLM)
    - AIImagen: Generates images with Stable Diffusion (uses stable diffusion XL running on cloudflare AI)
    - AIAudioTrancscribe: Transcribes audio when prompted (all audio files within 5 messages)

## Privacy considerations

With `AIEnabled`, the bot will send all messages from the set main channel to Google's Gemini API for processing. On free tier, Google may use this collected data to improve its models. Do not set the main channel to #general or similar, or modify the code to use Cloudflare AI instead. This may degrade performance.
