from telegram import Update
from telegram.ext import ContextTypes
import requests

CHAIN_DICT = {
    '5': {
        'prefix': 'gor'
    }
}


async def handle_ticket_buy_start(update: Update,
                                  context: ContextTypes.DEFAULT_TYPE):
    text = """
    Please add 0x6Dbd26Bca846BDa60A90890cfeF8fB47E7d0f22c to your safe. Reply 'delegate added' when done
    """
    await context.bot.send_message(chat_id=str(update.effective_chat.id),
                                   text=text)


async def handle_delegate_added(update: Update,
                                context: ContextTypes.DEFAULT_TYPE):
    text = """
    Please reply with your chain ID and address
    """
    await context.bot.send_message(chat_id=str(update.effective_chat.id),
                                   text=text)


async def propose_ticket_buy_transaction(update: Update,
                                         context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    chain_id, address = message_text.split(" ")
    response = await propose_transaction(chain_id, address)
    print('response', response)
    chain = CHAIN_DICT[chain_id]
    response_message = "Approve your transaction:" \
                       f"https://app.safe.global/transactions/queue?safe={chain['prefix']}:{address}"
    await context.bot.send_message(chat_id=str(update.effective_chat.id),
                                   text=str(response_message))
    await context.bot.send_message(chat_id=str(update.effective_chat.id),
                                   text="Reply paid once the transaction has been executed")



async def propose_transaction(chain_id, address):
    url = "http://localhost:5001/propose-transaction"

    # Create the request body
    payload = {
        "chain_id": chain_id,
        "address": address
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # Process the response
        print("Request was successful. Response:")
        print(response.json())  # Assuming the response is in JSON format
        return response.json()

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return e


def handle_ticket_purchase_complete(update: Update,
                                    context: ContextTypes.DEFAULT_TYPE):
    pass
