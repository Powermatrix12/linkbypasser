import os
import requests
from pyrogram import Client, filters

# Replace with your bot token from BotFather
API_ID = "your_api_id"  # Get from https://my.telegram.org
API_HASH = "your_api_hash"  # Get from https://my.telegram.org
BOT_TOKEN = "your_bot_token"  # Get from BotFather

# Initialize the Pyrogram Client
app = Client("shortlink_bypass_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to bypass short links
def bypass_shortlink(url):
    try:
        response = requests.get(url, allow_redirects=True)
        return response.url  # Returns the final URL after all redirects
    except Exception as e:
        return f"Error: {e}"

# Command handler for /start
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Hi! Send me a short link, and I'll give you the direct link.")

# Message handler for any text message
@app.on_message(filters.text)
def handle_message(client, message):
    url = message.text.strip()
    if url.startswith(("http://", "https://")):
        direct_link = bypass_shortlink(url)
        message.reply_text(f"Direct Link: {direct_link}")
    else:
        message.reply_text("Please send a valid URL starting with http:// or https://")

# Run the bot
print("Bot is running...")
app.run()
