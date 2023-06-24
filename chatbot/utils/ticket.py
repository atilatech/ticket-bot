from telegram import Update
from telegram.ext import ContextTypes


async def handle_ticket_buy(update: Update,
                      context: ContextTypes.DEFAULT_TYPE):

    text = """
    What is your chain and address?
    1. Gnosis Chain
    2. Goerli
    3. Polygon
    """
    await context.bot.send_message(chat_id=str(update.effective_chat.id),
                                   text=text)
