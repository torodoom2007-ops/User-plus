import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

# קריאת הנתונים הרגישים מתוך ההגדרות של Render
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE')  # מספר הטלפון שלך
TARGET_CHANNEL = 'https://t.me'

if not API_ID or not API_HASH or not PHONE_NUMBER:
    print("❌ שגיאה: לא הגדרת את TELEGRAM_API_ID, TELEGRAM_API_HASH או TELEGRAM_PHONE ב-Render!")
    exit(1)

# שימוש בתיקייה זמנית ב-Render כדי לשמור את קובץ החיבור
session_path = '/opt/render/project/src/session_file' if os.path.exists('/opt/render/project/src/') else 'session_file'
client = TelegramClient(session_path, int(API_ID), API_HASH)

async def main():
    print("[*] מתחיל תהליך התחברות לטלגרם...")
    
    # התחברות לשרתים
    await client.connect()
    
    # אם החשבון לא מחובר, נבקש קוד אימות דרך הטרמינל
    if not await client.is_user_authorized():
        print(f"[*] שולח קוד אימות למספר: {PHONE_NUMBER}")
        await client.send_code_request(PHONE_NUMBER)
        
        # הקוד יעצור כאן ויחכה שתכתוב את הקוד ב-Render Console
        code = input("🔄 הזן את קוד האימות שקיבלת מטלגרם בתוך האפליקציה: ")
        try:
            await client.sign_in(PHONE_NUMBER, code)
            print("✅ החשבון אומת וחובר בהצלחה!")
        except Exception as e:
            print(f"❌ אימות נכשל: {e}")
            return

    print(f"[*] מנסה להצטרף לערוץ: {TARGET_CHANNEL}...")
    try:
        await client(JoinChannelRequest(TARGET_CHANNEL))
        print("✅ ההצטרפות הצליחה! המשתמש החדש מופיע כעת בערוץ.")
    except Exception as e:
        print(f"❌ ההצטרפות נכשלה: {e}")

with client:
    client.loop.run_until_complete(main())
