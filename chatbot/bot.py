import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from utils.credentials import BOT_TOKEN
from utils.database import save_data
from utils.ticket import handle_ticket_buy_start, propose_ticket_buy_transaction, handle_ticket_purchase_complete

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHAIN, ADDRESS, DELEGATE, APPROVE = range(4)

chain_name_to_id = {
    "Gnosis Chain": "0x64",
    # "Gerli": "???",
    "Polygon": "0x89"
}


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text

    if len(message_text.split(' ')) == 3:  # ticket buy <event_id>
        await handle_ticket_buy_start(update, context)
    if message_text.lower() == 'delegate added':
        #
        pass
    if len(message_text.split(' ')) == 2:  # <chain_id> <address>
        await propose_ticket_buy_transaction(update, context)
    if message_text.lower() == 'done':
        await handle_ticket_purchase_complete(update, context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_welcome = f"""
           @atilaticketbot allows you to buy event tickets using crypto.
           """
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text=bot_welcome,
                                   reply_to_message_id=update.message.message_id)


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [list(chain_name_to_id.keys())]

    await update.message.reply_text(

        "Select your chain.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )

    return CHAIN


async def chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected chain and asks for the wallet address."""
    user = update.message.from_user
    text = update.message.text
    logger.info(f"Selected Chain: {text}. User: {user}")

    user_to_save = {
        'user_id': user.id,
        'chain_id': chain_name_to_id[text],
    }

    save_data(user_to_save)

    await update.message.reply_text("What is your wallet address?")

    return ADDRESS


async def address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the address and asks to delegate."""
    user = update.message.from_user
    wallet_address = update.message.text
    logger.info(f"Wallet address: {wallet_address}")

    await update.message.reply_text(
        "Next, add <...> as a delegate. Reply 'delegate added' when finished."
    )

    return DELEGATE


async def delegate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Confirms delegate added and asks user to approve payment."""
    user = update.message.from_user
    msg = update.message.text
    await update.message.reply_text(
        "Approve payment transaction: <link to transaction>. Reply 'paid' when finished."
    )

    return APPROVE


async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """User replied 'paid'. """
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("NFT Transfer Complete.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the transaction.", user.first_name)
    await update.message.reply_text(
        "Transaction cancelled.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    text_filter = filters.TEXT & ~filters.COMMAND

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("buy", buy)],
        states={
            CHAIN: [MessageHandler(text_filter, chain)],
            ADDRESS: [MessageHandler(text_filter, address)],
            DELEGATE: [MessageHandler(text_filter, delegate)],
            APPROVE: [MessageHandler(text_filter, approve)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('start', start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
