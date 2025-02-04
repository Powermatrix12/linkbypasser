# main.py
import os
import re
import base64
import requests
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Telegram Bot Token from environment variable
BOT_TOKEN = "7500719459:AAF7XpWQb6mnVFV7ZhU-OFEBMtsrTc8M5Is"

# Create the Application
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handler to start the bot
async def start(update: Update, context):
    await update.message.reply_text("Hello! Send me a File Store bot link, and I'll fetch the media for you.")

# Extract and decode file identifier from the link
def extract_file_command(link: str):
    match = re.search(r'start=([A-Za-z0-9-_]+)', link)
    if match:
        try:
            decoded_data = base64.urlsafe_b64decode(match.group(1)).decode('utf-8')
            return decoded_data
        except Exception as e:
            print(f"Decoding error: {e}")
    return None

async def handle_message(update: Update, context):
    message_text = update.message.text

    # Extract file command from the provided link
    file_command = extract_file_command(message_text)

    if not file_command:
        await update.message.reply_text("Invalid link. Please provide a valid File Store bot media link.")
        return

    # Interact with the file store bot
    bot_username = "Futa_Store_Robot"  # Replace with the appropriate bot username if needed

    try:
        # Send command to the file store bot to retrieve media
        bot_response = await context.bot.send_message(chat_id=f"@{bot_username}", text=f"/start {file_command}")

        # Listen for the file response
        await update.message.reply_text("Fetching media, please wait...")

        # Simulate download by waiting for the bot's response (this would need message polling in a real bot)
        # Example response handling (replace with better logic for production)
        media_url = f"https://example.com/download/{file_command}"  # Replace with real download logic
        response = requests.get(media_url)

        if response.status_code == 200:
            file_name = "downloaded_media_file"
            with open(file_name, "wb") as file:
                file.write(response.content)

            # Send the file back to the user
            await update.message.reply_document(document=InputFile(file_name))
            os.remove(file_name)
        else:
            await update.message.reply_text("Failed to download the file. Please try again.")

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Command and message handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == '__main__':
    print("Starting bot...")
    app.run_polling()
