import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
from keep_alive import keep_alive

keep_alive()
# Caesar cipher shift value
SHIFT = 3

# Function to encrypt text using Caesar cipher
def caesar_cipher(text, shift):
    result = []
    for char in text:
        if char.isalpha():  # Check if character is alphabetic
            offset = 65 if char.isupper() else 97
            encrypted_char = chr((ord(char) - offset + shift) % 26 + offset)
            result.append(encrypted_char)
    return ''.join(result)

# Function to handle /start command with reply keyboard
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            KeyboardButton("Encrypt Text"),
            KeyboardButton("Decrypt Text"),
        ],
        [
            KeyboardButton("Clear Session"),
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Welcome! Please choose an option below:", reply_markup=reply_markup)

# Function to handle text messages for encrypt and decrypt
async def handle_text(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text

    if user_input == "Encrypt Text":
        await update.message.reply_text("Please send the text to encrypt:")
        context.user_data['action'] = 'encrypt'

    elif user_input == "Decrypt Text":
        await update.message.reply_text("Please send the encrypted text to decrypt:")
        context.user_data['action'] = 'decrypt'

    elif user_input == "Clear Session":
        context.user_data.clear()  # Clear any stored data (like action type or text)
        await update.message.reply_text("Session cleared! You can start again by choosing an option.")
        return

    elif 'action' in context.user_data:
        text = update.message.text
        if context.user_data['action'] == 'encrypt':
            encrypted_text = caesar_cipher(text, SHIFT)
            await update.message.reply_text(f"Encrypted text:\n`{encrypted_text}`", parse_mode='Markdown')
        elif context.user_data['action'] == 'decrypt':
            decrypted_text = caesar_cipher(text, -SHIFT)
            await update.message.reply_text(f"Decrypted text:\n`{decrypted_text}`", parse_mode='Markdown')
        
        # Clear action after processing
        context.user_data.clear()
    else:
        await update.message.reply_text("Please choose an action first by clicking a button.")

# Main function to set up the bot
def main():
    # Set up logging to get errors if any
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Insert your bot's token here
    TOKEN = '8299566729:AAERe9_0TzUxqkxPS_NZEko3Ut23iBjrkyw'

    # Create Application object
    application = Application.builder().token(TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))  # Handle text input for encrypt and decrypt

    # Start polling to listen for updates
    application.run_polling()

if __name__ == '__main__':
    main()
