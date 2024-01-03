import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram.ext import filters, MessageHandler, ApplicationBuilder, CallbackQueryHandler, ContextTypes
import requests
from constants import API_KEY, LEO_ID, TCHEL_ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
account_keyboard = [
    [
        InlineKeyboardButton("Leo's", callback_data='leo'),
        InlineKeyboardButton("Tchel's", callback_data='tchel'),
    ],
    [InlineKeyboardButton("Joint account", callback_data='joint')],
]
account_keyboard_markup = InlineKeyboardMarkup(account_keyboard)

payment_keyboard = [
    [
        InlineKeyboardButton("Debit", callback_data='debit'),
        InlineKeyboardButton("Credit", callback_data='credit'),
    ],
    [InlineKeyboardButton("VR", callback_data='vr')],
]
payment_keyboard_markup = InlineKeyboardMarkup(payment_keyboard)


item = {}

async def process_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(context._chat_id)
    if chat_id == LEO_ID:
        item['user'] = 'leo'
    elif chat_id == TCHEL_ID:
        item['user'] = 'tchel'
    else:
        return
    text = update.message.text.split(" ")
    item['description'] = text[0]
    item['value'] = text[1]
    await update.message.reply_text('Which account?', reply_markup=account_keyboard_markup)

async def payment_type(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(chat_id=context._chat_id, text='How did you pay?', reply_markup=payment_keyboard_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")

    if query.message.reply_markup == account_keyboard_markup:
        item['account'] = query.data
        await payment_type(context)
    elif query.message.reply_markup == payment_keyboard_markup:
        item['payment'] = query.data
        await addItem(item)
        await context.bot.sendMessage(chat_id=context._chat_id, text='Entry added to the database! uwu')


async def addItem(item):
    requests.post("http://localhost:8080/dashboard/insert", json=item, headers ={'Content-Type': 'application/json'})




if __name__ == '__main__':
    application = ApplicationBuilder().token(API_KEY).build()

    item_handler = MessageHandler(filters.ALL, process_item)
    application.add_handler(item_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()