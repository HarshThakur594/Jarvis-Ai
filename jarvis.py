import requests
import datetime
import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

# 🔑 CONFIG (SAFE)
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# 🧠 AI FUNCTION
def ask_ai(user_text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": """
You are Jarvis, a smart and natural AI assistant.
 made/devlop/create by Harsh Tomar
Rules:
- Always reply in Hinglish (Hindi + English mix)
- Talk like a real human friend
- Keep tone natural
- Do NOT use emojis in every message
- Use emojis only when it truly fits
- Avoid forced jokes
- Understand casual conversation properly
- Give meaningful replies
"""
            },
            {"role": "user", "content": user_text}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=data)
        return res.json()['choices'][0]['message']['content']
    except:
        return "Thoda issue aa gaya, fir se try kar."

# 💬 TEXT HANDLER
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    # typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    await asyncio.sleep(1.5)

    if "time" in user_text:
        reply = "Abhi time hai " + datetime.datetime.now().strftime("%H:%M")
    elif "date" in user_text:
        reply = "Aaj ki date hai " + str(datetime.date.today())
    else:
        reply = ask_ai(user_text)

    await update.message.reply_text(reply)

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Jarvis online ho gaya.\nSeedha baat kar, main yahin hoon."
    )

# 🧠 MAIN
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_text))

print("Jarvis Bot Running...")
app.run_polling()