import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from utils.credentials import BOT_TOKEN
from utils.ticket import handle_ticket_buy

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_welcome = f"""
           @atilaticketbot allows you to buy event tickets using crypto.
           """
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text=bot_welcome,
                                   reply_to_message_id=update.message.message_id)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text

    if message_text.startswith('ticket'):
        await handle_ticket_buy(update, context)


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))

    application.run_polling()
