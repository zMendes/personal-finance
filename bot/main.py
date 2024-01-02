import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram.ext import filters, MessageHandler, ApplicationBuilder, CallbackQueryHandler, ContextTypes
from constants import API_KEY
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
import requests
account_keyboard = [
    [
        InlineKeyboardButton("Leo's", callback_data='1'),
        InlineKeyboardButton("Tchel's", callback_data='2'),
    ],
    [InlineKeyboardButton("Joint account", callback_data='3')],
]
account_keyboard_markup = InlineKeyboardMarkup(account_keyboard)

payment_keyboard = [
    [
        InlineKeyboardButton("Debit", callback_data='1'),
        InlineKeyboardButton("Credit", callback_data='2'),
    ],
    [InlineKeyboardButton("VR", callback_data='3')],
]
payment_keyboard_markup = InlineKeyboardMarkup(payment_keyboard)

async def process_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Which account?', reply_markup=account_keyboard_markup)


async def payment_type(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(chat_id=context._chat_id, text='How did you pay?', reply_markup=payment_keyboard_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")

    if query.message.reply_markup == account_keyboard_markup:
        await payment_type(context)
    elif query.message.reply_markup == payment_keyboard_markup:
        addItem("")

def addItem(item):
    pass




if __name__ == '__main__':
    application = ApplicationBuilder().token(API_KEY).build()

    item_handler = MessageHandler(filters.ALL, process_item)

    application.add_handler(item_handler)
    application.add_handler(CallbackQueryHandler(button))


    application.run_polling()