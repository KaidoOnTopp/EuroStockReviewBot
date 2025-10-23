import logging
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ===========================
# CONFIGURATION
# ===========================
TOKEN = "7840559432:AAGezhFNq11JEMYyAMbxbMpxzFeAY7LiJqo"
LOGO_PATH = r"C:\Users\Kaido\Desktop\Logo.jpg"
REVIEW_FOLDER = r"C:\Users\Kaido\Desktop\Nouveau dossier\Review"

# ===========================
# LOGGING
# ===========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ===========================
# AVIS PERSONNALISÉS
# ===========================
CUSTOM_REVIEW_TEXTS = [
    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nAmazing experience! My payment went through in seconds. Totally worth it!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nFast and professional service. Highly recommend Eurostock!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nPerfect! Everything went smoothly and securely. 10/10!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nExcellent support and reliable transfer. Will buy again!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nSuper fast and smooth experience. The best on Telegram!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nEurostock never disappoints. Instant delivery and top-notch communication!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nTransaction was instant and secure. Excellent quality as always!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nIncredible speed and reliability. Trustworthy every single time!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nProfessional service and great communication. Highly recommend!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nFast, smooth, and reliable. Eurostock is my go-to service!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nEverything was handled perfectly. Professional and trustworthy!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nOrder completed within minutes. Amazing support and results!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nEurostock is simply the best. Fast, legit, and friendly!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nReliable service every single time. Excellent team!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nMy favorite vendor. Always quick and safe transactions!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nSmooth process and very responsive team. A+ service!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nTop quality as always. Fast results and easy process.\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nThey really deliver what they promise. 100% reliable!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nQuick confirmation, legit service, and friendly support.\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nTrusted vendor. Everything went smoothly and instantly!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nVery reliable and professional. Highly recommend to everyone.\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nBest service on Telegram. Always delivers what’s promised.\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nLightning fast and professional. Couldn’t ask for better!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nCustomer service is outstanding. Always helpful and fast.\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nNever had a single issue. Reliable, quick and honest.\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nThe only service I trust. Always fast and professional.\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nOutstanding quality and speed. I’ll definitely be back!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nAlways on point. Clean, safe and very professional service!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",

    "⭐️⭐️⭐️⭐️⭐️\n<b>REVIEWED PRODUCT:</b> EUROSTOCK BILL SERVICE\n\nBest experience I’ve had online. Trusted and super fast!\n\n— <i>Verified Customer</i>\n\n💬 <b>Order now via</b> 👉 <a href='https://t.me/cvvskyy'>@cvvskyy</a>",
]


# ===========================
# CHARGE LES IMAGES
# ===========================
REVIEWS = []
image_files = sorted([f for f in os.listdir(REVIEW_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))])

for i, file in enumerate(image_files):
    text = CUSTOM_REVIEW_TEXTS[i] if i < len(CUSTOM_REVIEW_TEXTS) else CUSTOM_REVIEW_TEXTS[-1]
    REVIEWS.append({
        "photo": os.path.join(REVIEW_FOLDER, file),
        "caption": text
    })

# ===========================
# MENU PRINCIPAL
# ===========================
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, from_callback=False):
    """Affiche le menu principal avec logo et boutons."""
    keyboard = [
        [InlineKeyboardButton("🏠 Join Main Channel", url="https://t.me/eurostockv1")],
        [InlineKeyboardButton("🛒 Place an Order", url="https://t.me/cvvskyy")],
        [InlineKeyboardButton("⭐ Customer Reviews", callback_data="reviews_0")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "👋 <b>Welcome to Eurostock Official!</b>\n\n"
        "Your trusted source for fast, verified, and professional services.\n\n"
        "Use the buttons below to join our main channel, place your order, or explore client feedback. 👇"
    )

    if from_callback:
        query = update.callback_query
        await query.message.delete()
        with open(LOGO_PATH, "rb") as logo:
            await query.message.reply_photo(
                photo=InputFile(logo),
                caption=welcome_text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
    else:
        with open(LOGO_PATH, "rb") as logo:
            await update.message.reply_photo(
                photo=InputFile(logo),
                caption=welcome_text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )

# ===========================
# AFFICHAGE DES AVIS
# ===========================
async def show_review(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int):
    """Affiche une review spécifique avec navigation."""
    query = update.callback_query
    await query.answer()

    # Effet "chargement"
    loading = await query.message.reply_text("⏳ Loading verified reviews...")
    await asyncio.sleep(1)
    await loading.delete()

    review = REVIEWS[page]
    total = len(REVIEWS)

    keyboard = [
        [
            InlineKeyboardButton("⏪", callback_data=f"reviews_0"),
            InlineKeyboardButton("◀️", callback_data=f"reviews_{max(page-1, 0)}"),
            InlineKeyboardButton(f"{page+1}/{total}", callback_data="none"),
            InlineKeyboardButton("▶️", callback_data=f"reviews_{min(page+1, total-1)}"),
            InlineKeyboardButton("⏩", callback_data=f"reviews_{total-1}")
        ],
        [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(review["photo"], "rb") as img:
        await query.message.reply_photo(
            photo=InputFile(img),
            caption=review["caption"],
            parse_mode="HTML",
            reply_markup=reply_markup
        )

# ===========================
# CALLBACKS
# ===========================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data.startswith("reviews_"):
        page = int(data.split("_")[1])
        await show_review(update, context, page)
    elif data == "none":
        await query.answer("Use the arrows to navigate pages.", show_alert=False)
    elif data == "main_menu":
        await show_main_menu(update, context, from_callback=True)

# ===========================
# MAIN
# ===========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", lambda u, c: show_main_menu(u, c)))
    app.add_handler(CallbackQueryHandler(button_callback))
    print(f"🤖 Eurostock Bot is running with {len(REVIEWS)} reviews...")
    app.run_polling()

if __name__ == "__main__":
    main()
