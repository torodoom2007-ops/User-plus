import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

# קריאת הנתונים הרגישים מתוך ההגדרות של Render (מונע חשיפה שלהם בגיטהאב)
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
# הקישור לערוץ שביקשת
TARGET_CHANNEL = 'https://t.me/ask_movie_MT'

# בדיקה שהגדרת את הנתונים ב-Render
if not API_ID or not API_HASH:
    print("❌ שגיאה: לא הגדרת את TELEGRAM_API_ID או TELEGRAM_API_HASH ב-Render!")
    exit(1)

# יצירת הלקוח של טלגרם. הקובץ 'session_file.session' ייווצר אוטומטית ברגע שתתחבר בפעם הראשונה
client = TelegramClient('session_file', int(API_ID), API_HASH)

async def main():
    print("[*] מתחבר לטלגרם...")
    await client.connect()
    
    # בדיקה האם המשתמש כבר מחובר (מאומת)
    if not await client.is_user_authorized():
        print("❌ החשבון אינו מחובר! יש להריץ את הקוד פעם אחת מקומית במחשב כדי להזין קוד אימות.")
        return

    print(f"[*] מנסה להצטרף לערוץ: {TARGET_CHANNEL}...")
    try:
        # שליחת בקשת הצטרפות לערוץ
        await client(JoinChannelRequest(TARGET_CHANNEL))
        print("✅ ההצטרפות הצליחה! המשתמש החדש מופיע כעת בערוץ.")
    except Exception as e:
        print(f"❌ ההצטרפות נכשלה. שגיאה: {e}")

# הרצת התוכנית
with client:
    client.loop.run_until_complete(main())
