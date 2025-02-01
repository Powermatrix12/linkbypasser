import os
import requests
from pyrogram import Client, filters

# Replace with your bot token from BotFather
API_ID = "23342871"  # Get from https://my.telegram.org
API_HASH = "7405511dc0b47d778640f913cb46a65a"  # Get from https://my.telegram.org
BOT_TOKEN = "7201537576:AAEPVBkJ4fGqLCBItjFDUcfVbZAMIeCzhwU"  # Get from BotFather

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
