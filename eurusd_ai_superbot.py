import telegram
from telegram.ext import Updater, CommandHandler
import requests
from datetime import datetime
import csv
import os

# 1. توكن البوت
BOT_TOKEN = '8162123139:AAEeIFt8Wz8TQYAgkCfhJUZGImlZM5-uCOM'

# 2. رابط API للسيرفر المحلي
SERVER_URL = 'http://127.0.0.1:5005/eurusd'

# 3. اسم ملف السجل
CSV_FILENAME = "eurusd_analysis_log.csv"

# 4. كتابة السطر إلى ملف CSV
def log_to_csv(time, price, prediction):
    file_exists = os.path.isfile(CSV_FILENAME)
    with open(CSV_FILENAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Time", "Price", "Prediction"])
        writer.writerow([time, price, prediction])

# 5. جلب التحليل من السيرفر
def get_analysis():
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"تعذر الوصول إلى الخادم (status code: {response.status_code})"}
    except Exception as e:
        return {"error": str(e)}

# 6. عند تنفيذ أمر /analyze
def analyze(update, context):
    result = get_analysis()
    now = datetime.now().strftime("%H:%M:%S")
    msg = f"🕐 التوقيت: {now}\n"

    if "error" in result:
        msg += f"❌ {result['error']}"
    else:
        price = result.get("price", "غير متاح")
        prediction = result.get("prediction", "غير متاح")

        msg += f"📉 EUR/USD: {price}\n"
        msg += f"🤖 التوقع: {prediction}"

        # حفظ في ملف CSV
        log_to_csv(now, price, prediction)

    update.message.reply_text(msg)

# 7. تشغيل البوت
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("analyze", analyze))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
