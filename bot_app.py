import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Store user IDs here (basic version)
users = set()

logging.basicConfig(level=logging.INFO)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    users.add(user_id)

    keyboard = [
        [InlineKeyboardButton("💪 Whey Protein", callback_data="whey")],
        [InlineKeyboardButton("⚡ Creatine", callback_data="creatine")],
        [InlineKeyboardButton("🔥 Fat Burners", callback_data="fat")],
        [InlineKeyboardButton("🥤 Pre-Workout", callback_data="pre")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to Fitness Deals Bot! 👋\nChoose a category below:",
        reply_markup=reply_markup
    )

# Handle button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "whey":
        await query.message.reply_text("🔥 Best Whey Deals:\nhttps://your-affiliate-link")
    elif query.data == "creatine":
        await query.message.reply_text("⚡ Creatine Deals:\nhttps://your-affiliate-link")
    elif query.data == "fat":
        await query.message.reply_text("🔥 Fat Burners:\nhttps://your-affiliate-link")
    elif query.data == "pre":
        await query.message.reply_text("🥤 Pre-Workout Deals:\nhttps://your-affiliate-link")

# Run the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
