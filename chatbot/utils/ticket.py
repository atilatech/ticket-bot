from telegram import Update
from telegram.ext import ContextTypes


async def handle_ticket_buy_start(update: Update,
                                  context: ContextTypes.DEFAULT_TYPE):
    text = """
    What is your chain and address?
    1. Gnosis Chain
    2. Goerli
    3. Polygon
    """
    await context.bot.send_message(chat_id=str(update.effective_chat.id),
                                   text=text)


def propose_ticket_buy_transaction(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE):
    # send POST Request to propose a transaction
    pass


def handle_ticket_purchase_complete(update: Update,
                                    context: ContextTypes.DEFAULT_TYPE):
    pass
