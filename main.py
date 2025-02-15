from telethon import TelegramClient, events
import re
import os
import logging
import asyncio

# إعدادات تسجيل الأخطاء (Logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# جلب القيم من المتغيرات البيئية بدلاً من كتابتها مباشرة (أمان أكثر)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNELS = list(map(int, os.getenv("SOURCE_CHANNELS").split(',')))  # تحويل النص إلى قائمة أرقام
TARGET_CHANNEL = int(os.getenv("TARGET_CHANNEL"))

# قائمة التصنيفات
CATEGORIES = {
    'أخبار': ['خبر', 'عاجل', 'سياسة', 'اقتصاد'],
    'رياضة': ['مباراة', 'كرة قدم', 'الدوري', 'المنتخب'],
    'ترفيه': ['فيلم', 'مسلسل', 'أغنية', 'حفلة'],
    'تعليم': ['دورة', 'محاضرة', 'تعليم', 'مدرسة', 'جامعة']
}

def classify_text(text):
    """تحديد تصنيف النص بناءً على الكلمات المفتاحية"""
    for category, keywords in CATEGORIES.items():
        if any(re.search(rf'\b{keyword}\b', text, re.IGNORECASE) for keyword in keywords):
            return category
    return 'عام'

client = TelegramClient('bot_session', API_ID, API_HASH)

async def start_bot():
    try:
        await client.start(bot_token=BOT_TOKEN)
        logger.info("✅ البوت متصل وجاهز للعمل على Koyeb...")
    except Exception as e:
        logger.error(f"❌ خطأ أثناء بدء البوت: {e}")
        raise e

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    try:
        message = event.message
        text = message.text if message.text else getattr(message, 'caption', '')  # جلب النص أو التسمية التوضيحية
        media = message.media  # التحقق مما إذا كانت الرسالة تحتوي على ملف

        if text:
            category = classify_text(text)
            formatted_message = f'📌 التصنيف: {category}\n\n{text}'
        else:
            formatted_message = '📌 التصنيف: غير محدد (ملف بدون وصف)'

        if media:  # إذا كانت الرسالة تحتوي على وسائط (صور، فيديو، ملفات، إلخ)
            await client.send_message(TARGET_CHANNEL, formatted_message, file=media)
            logger.info(f"📤 تم إرسال ملف{' مع وصف' if text else ' بدون وصف'} إلى القناة المستهدفة.")
        else:
            await client.send_message(TARGET_CHANNEL, formatted_message)
            logger.info(f"📤 تم إرسال رسالة نصية فقط إلى القناة المستهدفة.")

    except Exception as e:
        logger.error(f"❌ خطأ أثناء معالجة الرسالة: {e}")

async def main():
    await start_bot()
    await client.run_until_disconnected()

# تشغيل البوت في Koyeb بشكل غير متزامن
if __name__ == "__main__":
    asyncio.run(main())
