import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# =========================
# BOT TOKEN
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")

# =========================
# DEALS DATABASE
# =========================
DEALS = {
    "creatine": [
        # ---- HyugaLife (High Commission) ----
        {
            "title": "HealthKart Creatine Monohydrate 100g",
            "price": "₹459",
            "price_per_100g": 459,
            "platform": "HyugaLife",
            "tag": "🔥 Cheapest",
            "link": "https://hyugalife.com/?utm_source=Cashkaro&utm_term=ENKR20251213A1734192911"
        },
        {
            "title": "BigMuscles Creatine 250g",
            "price": "₹749",
            "price_per_100g": 300,
            "platform": "HyugaLife",
            "tag": "💸 Best Value",
            "link": "https://hyugalife.com/?utm_source=Cashkaro&utm_term=ENKR20251213A1734192911"
        },
        {
            "title": "Fast&Up Creatine 200g",
            "price": "₹699",
            "price_per_100g": 349,
            "platform": "HyugaLife",
            "tag": "⚡ Limited Deal",
            "link": "https://hyugalife.com/?utm_source=Cashkaro&utm_term=ENKR20251213A1734192911"
        },

        # ---- Amazon (Trust + Backup) ----
        {
            "title": "MuscleBlaze Creatine 250g",
            "price": "₹899",
            "price_per_100g": 359,
            "platform": "Amazon",
            "tag": "🏆 Popular Brand",
            "link": "https://hyugalife.com/?utm_source=Cashkaro&utm_term=ENKR20251213A1734192911"
        },
        {
            "title": "Optimum Nutrition Creatine 300g",
            "price": "₹1,099",
            "price_per_100g": 366,
            "platform": "Amazon",
            "tag": "⭐ Best Rated",
            "link": "https://hyugalife.com/?utm_source=Cashkaro&utm_term=ENKR20251213A1734192911"
        }
    ],

    # You can add whey / preworkout / fatburner same way
}

# =========================
# START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Creatine", callback_data="creatine")],
        [InlineKeyboardButton("🥛 Whey Protein", callback_data="whey")],
        [InlineKeyboardButton("🔥 Fat Burners", callback_data="fatburner")],
        [InlineKeyboardButton("☕ Pre-Workout", callback_data="preworkout")]
    ]

    await update.message.reply_text(
        "🏋️ *Welcome to Fitness Deals Bot*\n\n"
        "Select a category to get the *best deals right now* 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# =========================
# DEAL SELECTION LOGIC
# =========================
def get_top_5(deals):
    hyuga = [d for d in deals if d["platform"] == "HyugaLife"]
    amazon = [d for d in deals if d["platform"] == "Amazon"]

    hyuga_sorted = sorted(hyuga, key=lambda x: x["price_per_100g"])
    amazon_sorted = sorted(amazon, key=lambda x: x["price_per_100g"])

    result = []

    # Always include cheapest overall
    result.append(min(deals, key=lambda x: x["price_per_100g"]))

    # Add up to 3 HyugaLife deals
    for d in hyuga_sorted:
        if d not in result and len(result) < 4:
            result.append(d)

    # Fill remaining slots with Amazon
    for d in amazon_sorted:
        if d not in result and len(result) < 5:
            result.append(d)

    return result

# =========================
# CATEGORY HANDLER
# =========================
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    category = query.data
    await query.answer()

    deals = DEALS.get(category)

    if not deals:
        await query.message.reply_text(
            "⚠️ No active deals right now.\nPlease check again later."
        )
        return

    top_deals = get_top_5(deals)

    await query.message.reply_text(
        f"🔥 *Top 5 Best {category.upper()} Deals Right Now* 🔥",
        parse_mode="Markdown"
    )

    for i, deal in enumerate(top_deals, 1):
        msg = (
            f"*{i}. {deal['title']}*\n"
            f"{deal['tag']}\n"
            f"💰 Price: {deal['price']}\n"
            f"🏪 Platform: {deal['platform']}\n"
            f"👉 Buy Now: {deal['link']}\n"
            f"—————————————"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

# =========================
# MAIN
# =========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(category_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
