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
from utils.ticket import handle_ticket_buy_start, propose_ticket_buy_transaction, handle_ticket_purchase_complete, \
    handle_delegate_added

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
        await handle_delegate_added(update, context)
    if len(message_text.split(' ')) == 2:  # <chain_id> <address>
        await propose_ticket_buy_transaction(update, context)
    if message_text.lower() == 'done':
        await handle_ticket_purchase_complete(update, context)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    text_filter = filters.TEXT & ~filters.COMMAND

    application.add_handler(MessageHandler(text_filter, chat))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
