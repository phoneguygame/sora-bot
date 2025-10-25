import telebot
from openai import OpenAI
import os

# 🔑 Токены
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "👋 Привет! Отправь мне описание, и я создам изображение 🎨")

@bot.message_handler(func=lambda m: True)
def generate_image(msg):
    prompt = msg.text
    bot.send_message(msg.chat.id, "⏳ Генерирую изображение, подожди немного...")

    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_url = response.data[0].url
        bot.send_photo(msg.chat.id, image_url, caption="✨ Готово!")

    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ Ошибка: {e}")

bot.polling(none_stop=True)
