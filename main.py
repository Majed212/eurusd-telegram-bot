import os
import logging
import datetime
from threading import Thread
from flask import Flask, jsonify
from telegram.ext import Updater, CommandHandler
from eurusd_ai_server import fetch_and_predict

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 5000))

# Flask app
app = Flask(__name__)

# Telegram bot
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    update.message.reply_text("👋 أهلاً! ارسل /analyze للحصول على تحليل EUR/USD مع التعلّم الذاتي.")

def analyze(update, context):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = fetch_and_predict()
    price = result['price']
    predicted = result['predicted_price']
    trend = result['trend']
    msg = f"🕒 {now}\n💶 السعر الحالي EUR/USD: {price}\n🔮 السعر المتوقع: {predicted}\n🤖 الاتجاه: {trend}"
    update.message.reply_text(msg)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("analyze", analyze))

def run_bot():
    updater.start_polling()
    updater.idle()

Thread(target=run_bot, daemon=True).start()

@app.route('/')
def home():
    return "EUR/USD Self-Learning Bot is running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)