import requests
import pytesseract
from PIL import Image
from io import BytesIO
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ توكن البوت حقك
TELEGRAM_BOT_TOKEN = "7498674497:AAHaYtqJJVc8reAZ4O198hn9Wb_WPBWOLcM"
REDEEM_URL = "https://wos-giftcode.centurygame.com"
ids_list = ["225281098", "223118226"]
session = requests.Session()

async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❌ أرسل الكود بهذي الطريقة:\n/redeem CODE1234")
        return

    code = context.args[0]
    results = []

    for player_id in ids_list:
        try:
            # تحميل صورة الكابتشا
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            captcha_resp = session.get(f"{REDEEM_URL}/captcha", headers=headers, stream=True)
            captcha_resp.raise_for_status()
            img = Image.open(BytesIO(captcha_resp.content))

            # التعرف على النص في الكابتشا
            captcha_text = pytesseract.image_to_string(img).strip()
            print(f"🔤 الكابتشا المقروءة: {captcha_text}")

            # إرسال الطلب
            resp = session.post(f"{REDEEM_URL}/redeem", data={
                "uid": player_id,
                "giftCode": code,
                "captcha": captcha_text
            })

            if "success" in resp.text:
                results.append(f"✅ {player_id}: تم التفعيل")
            else:
                results.append(f"❌ {player_id}: فشل التفعيل")

        except Exception as e:
            results.append(f"❌ {player_id}: خطأ أثناء التنفيذ - {e}")

    report = "\n".join(results)
    await update.message.reply_text(f"🎁 النتائج:\n{report}")

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("redeem", redeem))
app.run_polling()
