from telegram import *
from telegram.ext import *
import requests
import json
from types import SimpleNamespace
import math
import random

domain = "https://api.chootc.com"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Tham gia @exchangemoneyvn để mua bán, trao đổi USDT số lượng lớn!", parse_mode=constants.ParseMode.HTML)


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    chat_id = update.effective_chat.id
    print(chat_id)

app = ApplicationBuilder().token(
    "6768614811:AAEhD1YY1yfsVXEV41gLeXCSw_rQXgm18MM").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, messageHandler))


# auto send message
async def callback_minute(context: ContextTypes.DEFAULT_TYPE):

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='Xem tỷ giá', url='https://mmo4me.co'),
          InlineKeyboardButton(text='Mua bán PAYPAL', url='https://mmo4me.co')]])

    buy = requests.get(
        f"{domain}/api/p2p?type=buy&asset=usdt&fiat=vnd&page=1")
    sell = requests.get(
        f"{domain}/api/p2p?type=sell&asset=usdt&fiat=vnd&page=1")

    buy_price = buy.json()['data'][8]['adv']['price']
    sell_price = sell.json()['data'][8]['adv']['price']

    message = f"<b>USDT</b>\nBán: <b>{int(buy_price):,} VND</b>\nMua: <b>{int(sell_price):,} VND</b>\n\nXem tỷ giá miễn phí tại:\nhttps://mmo4me.co"

    try:
        mmo = requests.get(f"{domain}/api/setup/mmo")
        last_msg_id = mmo.json()["value"]

        await context.bot.delete_message(message_id=last_msg_id, chat_id='-1001845629407')
        msg = await context.bot.send_message(chat_id='-1001845629407', text=message, reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML, disable_web_page_preview=True)

        requests.put(f"{domain}/api/setup/mmo", {'value': msg.message_id})
    except:

        msg = await context.bot.send_message(chat_id='-1001845629407', text=message, reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML, disable_web_page_preview=True)
        requests.put(f"{domain}/api/setup/mmo", {'value': msg.message_id})


job_queue = app.job_queue

job_minute = job_queue.run_repeating(callback_minute, interval=60, first=10)

app.run_polling()
