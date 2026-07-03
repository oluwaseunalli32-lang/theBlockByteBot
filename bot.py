import os
import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fallback token for local testing; Render will use the Environment Variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_LOCAL_TEST_TOKEN")

# Dictionary of some starter crypto terms
CRYPTO_TERMS = {
    "blockchain": (
        "<b>Blockchain</b>\n\n"
        "A decentralized, distributed ledger that records the provenance of a digital asset. "
        "In simple terms, it's a shared database secure by cryptography where data is stored in blocks "
        "and chained together chronologically."
    ),
    "gas": (
        "<b>Gas Fee</b>\n\n"
        "The payments made by users to compensate for the computing energy required to process and validate "
        "transactions on a blockchain network, like Ethereum."
    ),
    "liquidity": (
        "<b>Liquidity</b>\n\n"
        "The ease with which a cryptocurrency or token can be converted into another cryptocurrency or fiat cash "
        "without impacting its market price."
    )
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_text = (
        f"Welcome <b>{user.first_name}</b> to <b>BlockByteBot</b>! 🚀\n\n"
        "I am your pocket-sized Web3 professor. Use these commands to learn:\n"
        "/learn - Get a random crypto term\n"
        "/blockchain - Learn about Blockchains\n"
        "/gas - Learn about Gas Fees\n"
        "/liquidity - Learn about Liquidity"
    )
    await update.message.reply_text(text=welcome_text, parse_mode=ParseMode.HTML)

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a general overview message or random term choice."""
    text = (
        "💡 <b>BlockByte Quick Tip:</b>\n\n"
        "Always research a project's fundamental utility before investing! "
        "Try typing commands like /blockchain or /gas to study specific definitions."
    )
    await update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

async def term_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Dynamically handle requested crypto terms based on the command used."""
    command = update.message.text.split()[0].replace("/", "").lower()
    
    if command in CRYPTO_TERMS:
        await update.message.reply_text(text=CRYPTO_TERMS[command], parse_mode=ParseMode.HTML)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("learn", learn))
    
    # Register handlers for your specific crypto terms
    for term in CRYPTO_TERMS.keys():
        application.add_handler(CommandHandler(term, term_handler))

    # Run the bot via long polling (Perfect for Render Background Workers)
    logger.info("BlockByteBot started successfully. Listening for messages...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
