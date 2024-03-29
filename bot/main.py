import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram.ext import filters, MessageHandler, ApplicationBuilder, CallbackQueryHandler, ContextTypes
import requests
from constants import API_KEY, LEO_ID, TCHEL_ID, WRONG_FORMAT


class TelegramBot():
    def __init__(self) -> None:
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.account_keyboard = [
            InlineKeyboardButton("Leo's", callback_data='leo'),
            InlineKeyboardButton("Tchel's", callback_data='tchel'),
            InlineKeyboardButton("Joint account", callback_data='joint')
        ],
        self.account_keyboard_markup = InlineKeyboardMarkup(
            self.account_keyboard)

        self.payment_keyboard = [
            InlineKeyboardButton("Debit", callback_data='debit'),
            InlineKeyboardButton("Credit", callback_data='credit'),
            InlineKeyboardButton("VR", callback_data='vr')
        ],
        self.payment_keyboard_markup = InlineKeyboardMarkup(
            self.payment_keyboard)

        application = ApplicationBuilder().token(API_KEY).build()
        item_handler = MessageHandler(filters.ALL, self.process_item)
        application.add_handler(item_handler)
        application.add_handler(CallbackQueryHandler(self.button))
        application.run_polling()

    async def process_item(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = str(context._chat_id)
        self.item = {}
        if chat_id == LEO_ID:
            self.item['user'] = 'leo'
        elif chat_id == TCHEL_ID:
            self.item['user'] = 'tchel'
        else:
            return

        text = [x.strip() for x in update.message.text.lower().split(',')]

        try:
            if text[0] == 'fatura':
                self.item['type'] = 'credit_card_bill'
                self.item['account'] = self.item['user']
            elif text[0] == 'recarga':
                self.item['type'] = 'recharge'
                self.item['account'] = f"{self.item['user']}-vr"
                self.item['value'] = text[1]
            elif text[0] == 'investimento':
                self.item['type'] = 'investment'
                self.item['value'] = float(text[1])
                self.item['account'] = self.item['user']
                await self.sendItem(self.item, context)
            elif text[0] == 'transferencia':
                self.item['account'] = self.item['user']
                if text[1] == self.item['user']:
                    self.item['type'] = 'transfer_in'
                    self.item['target_account'] = self.item['user']
                else:
                    self.item['type'] = 'transfer_out'
                    if text[1] in ['casa', 'joint', 'home']:
                        self.item['target_account'] = 'joint'
                    elif text[1] == 'tchel':
                        self.item['target_account'] = 'tchel'
                    else:
                        self.item['target_account'] = 'leo'
                self.item['value'] = float(text[2])
                await self.sendItem(self.item, context)

            elif len(text) != 2:
                raise (SyntaxError)
            else:
                self.item['type'] = 'expenses'
                self.item['description'] = text[0]
                self.item['value'] = float(text[1])
                await update.message.reply_text('Which account?', reply_markup=self.account_keyboard_markup)

        except:
            await context.bot.sendMessage(chat_id=context._chat_id, text=WRONG_FORMAT)

    async def payment_type(self, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.sendMessage(chat_id=context._chat_id, text='How did you pay?',
                                      reply_markup=self.payment_keyboard_markup)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query

        await query.answer()
        await query.edit_message_text(text=f"Selected option: {query.data}")

        if query.message.reply_markup == self.account_keyboard_markup:
            self.item['account'] = query.data
            await self.payment_type(context)
        elif query.message.reply_markup == self.payment_keyboard_markup:
            self.item['payment'] = query.data
            await self.sendItem(self.item, context)

    async def sendItem(self, item, context):
        print(item)
        requests.post("http://localhost:8080/dashboard/insert",
                      json=item, headers={'Content-Type': 'application/json'})
        await context.bot.sendMessage(chat_id=context._chat_id, text='Entry added to the database! uwu')



if __name__ == '__main__':

    bot = TelegramBot()
