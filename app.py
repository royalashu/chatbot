from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext


# Bot Token (Replace with your friend's bot token)
BOT_TOKEN = "1758801861:AAHev6ksknIaiQK7O04MTHHLGCpPV8S77Zk"

# Your Friend's Telegram ID (Only they can reply)
OWNER_ID = 1675462613  # Replace with your friend's Telegram user ID

# Dictionary to track conversations (User ID -> Forwarded Message ID)
user_conversations = {}

async def handle_user_message(update: Update, context: CallbackContext):
    """Handles messages from users and forwards them to the owner."""
    user_id = update.message.chat_id
    message = update.message

    # Forward message to the owner
    forwarded_message = await context.bot.forward_message(chat_id=OWNER_ID, from_chat_id=user_id, message_id=message.message_id)

    # Store mapping: Forwarded message ID (in owner's chat) -> Original user ID
    user_conversations[forwarded_message.message_id] = user_id

async def handle_owner_reply(update: Update, context: CallbackContext):
    """Handles replies from the owner and forwards them to the correct user."""
    if update.message.chat_id != OWNER_ID:
        return  # Ignore messages from others

    # Ensure the reply is to a forwarded message
    if update.message.reply_to_message and update.message.reply_to_message.message_id in user_conversations:
        user_id = user_conversations[update.message.reply_to_message.message_id]

        # Send the reply back to the original user
        if update.message.text:
            await context.bot.send_message(chat_id=user_id, text=update.message.text)
        elif update.message.photo:
            await context.bot.send_photo(chat_id=user_id, photo=update.message.photo[-1].file_id, caption=update.message.caption)
        elif update.message.video:
            await context.bot.send_video(chat_id=user_id, video=update.message.video.file_id, caption=update.message.caption)
        elif update.message.sticker:
            await context.bot.send_sticker(chat_id=user_id, sticker=update.message.sticker.file_id)
        elif update.message.animation:
            await context.bot.send_animation(chat_id=user_id, animation=update.message.animation.file_id)
        elif update.message.document:
            await context.bot.send_document(chat_id=user_id, document=update.message.document.file_id, caption=update.message.caption)

async def start(update: Update, context: CallbackContext):
    """Command to check if the bot is online."""
    await update.message.reply_text("Bot is running and ready!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Start command
    app.add_handler(MessageHandler(filters.Command("start"), start))

    # Handle messages from users (text, media)
    app.add_handler(MessageHandler(filters.ALL & ~filters.Chat(OWNER_ID), handle_user_message))
    
    # Handle replies from the owner
    app.add_handler(MessageHandler(filters.ALL & filters.Chat(OWNER_ID), handle_owner_reply))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
