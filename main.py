from telethon import TelegramClient, events
import json
import re
from textblob import TextBlob

# إعدادات البوت
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
BOT_TOKEN = 'YOUR_BOT_TOKEN'
SOURCE_CHANNELS = [-1001234567890]  # ضع معرف القنوات هنا
TARGET_CHANNEL = -1009876543210  # ضع معرف القناة المستهدفة هنا

# قائمة التصنيفات
CATEGORIES = {
    'أخبار': ['خبر', 'عاجل', 'سياسة', 'اقتصاد'],
    'رياضة': ['مباراة', 'كرة قدم', 'الدوري', 'المنتخب'],
    'ترفيه': ['فيلم', 'مسلسل', 'أغنية', 'حفلة'],
    'تعليم': ['دورة', 'محاضرة', 'تعليم', 'مدرسة', 'جامعة']
}

def classify_text(text):
    for category, keywords in CATEGORIES.items():
        if any(re.search(rf'\b{keyword}\b', text, re.IGNORECASE) for keyword in keywords):
            return category
    return 'عام'

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    message = event.message
    text = message.text or message.caption or ''
    category = classify_text(text)
    
    formatted_message = f'📌 التصنيف: {category}\n\n{text}'
    await client.send_message(TARGET_CHANNEL, formatted_message, file=message.media)
    
print("✅ البوت يعمل...")
client.run_until_disconnected()
