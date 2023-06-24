from telegram import Update
from telegram.ext import ContextTypes


async def handle_ticket_buy(update: Update,
                      context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=str(update.effective_chat.id),
                                   text='What is your address?')
