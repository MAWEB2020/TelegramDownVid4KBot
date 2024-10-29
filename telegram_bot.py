import os
import json
import instaloader
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Initialize Instaloader
insta_loader = instaloader.Instaloader()

# Define the path to save downloaded videos
DOWNLOAD_PATH = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_PATH, exist_ok=True)  # Create the folder if it doesn’t exist

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Send me a video link from Instagram, TikTok, Facebook, or YouTube to download.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text

    try:
        if "instagram" in url:
            insta_loader.download_profile(url, profile_pic_only=True)
            await update.message.reply_text("Instagram download feature is still under development.")

        elif "youtube" in url:
            # Use yt-dlp for YouTube downloads
            ydl_opts = {
                'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),  # Save in DOWNLOAD_PATH with video title
                'format': 'best',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            await update.message.reply_text("Downloaded YouTube video!")

        # Add more platforms similarly

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

# Define the Vercel handler
async def handler(request):
    if request.method == "POST":
        body = await request.json()
        token = "7721757764:AAFs3j-fo0DnzXucZwDtRstPB07ZGm6j4EM"
        application = Application.builder().token(token).build()

        # Simulate the update received from Telegram
        update = Update.de_json(body, application.bot)

        # Handle the update
        await application.update_queue.put(update)

        return json.dumps({"status": "success"})

    return json.dumps({"status": "invalid method"})

# You can add the entry point for the serverless function
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(handler, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
