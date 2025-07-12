
import requests
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# بيانات البوت
TELEGRAM_BOT_TOKEN = "7498674497:AAHaYtqJJVc8reAZ4O198hn9Wb_WPBWOLcM"
REDEEM_URL = "https://wos-giftcode.centurygame.com"
ids_list = ["225281098", "223118226"]
session = requests.Session()
pending_redeem = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != update.message.chat.id:
        await update.message.reply_text("🚫 هذا البوت مخصص فقط للإدمن.")
        return
    await update.message.reply_text("👋 هلا يوسف ❤️\nاكتب الكود اللي تبغى أوزعه على الأعضاء:")

async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != update.message.chat.id:
        await update.message.reply_text("🚫 هذا البوت مخصص فقط للإدمن.")
        return

    if len(context.args) == 0:
        await update.message.reply_text("❌ أرسل الكود بهذي الطريقة:\n/redeem CODE1234")
        return

    code = context.args[0]
    pending_redeem[user_id] = {"code": code}

    captcha_resp = session.get(f"{REDEEM_URL}/captcha", stream=True)
    with open("captcha.jpg", "wb") as f:
        for chunk in captcha_resp.iter_content(1024):
            f.write(chunk)

    await update.message.reply_photo(photo=open("captcha.jpg", "rb"),
                                     caption="📸 اكتب الكابتشا هنا:")

async def get_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in pending_redeem:
        await update.message.reply_text("❌ ما فيه كود محفوظ. ابدأ من جديد واكتب الكود أول.")
        return

    captcha_text = update.message.text.strip()
    code = pending_redeem[user_id]["code"]
    results = []

    for player_id in ids_list:
        resp = session.post(f"{REDEEM_URL}/redeem", data={
            "uid": player_id,
            "giftCode": code,
            "captcha": captcha_text
        })
        if "success" in resp.text:
            results.append(f"✅ {player_id}: تم التفعيل")
        else:
            results.append(f"❌ {player_id}: فشل التفعيل")

    report = "\n".join(results)
    await update.message.reply_text(f"🎁 النتائج:\n{report}")

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("redeem", redeem))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_captcha))
app.run_polling()
