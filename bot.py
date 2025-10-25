import telebot
import openai
import os

# 🔑 Токены
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Укажи в Render -> Environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "👋 Привет! Отправь описание — я создам изображение 🎨")

@bot.message_handler(func=lambda m: True)
def generate_image(msg):
    prompt = msg.text
    bot.send_message(msg.chat.id, "⏳ Генерирую изображение, подожди немного...")

    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response["data"][0]["url"]
        bot.send_photo(msg.chat.id, image_url, caption="✨ Готово!")

    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ Ошибка: {e}")

bot.polling(none_stop=True)
