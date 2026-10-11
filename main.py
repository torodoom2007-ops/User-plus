import os
import asyncio
import time
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE')
TELEGRAM_CODE = os.getenv('TELEGRAM_CODE') # קריאת הקוד מכפתור ההגדרות
TARGET_CHANNEL = 'https://t.me'

client = TelegramClient('session_file', int(API_ID), API_HASH)

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        if not TELEGRAM_CODE:
            print("========================================")
            print(f"⚠️ שולח קוד אימות למספר: {PHONE_NUMBER}")
            print("1. בדוק את אפליקציית טלגרם וקבל את הקוד.")
            print("2. כנס להגדרות Environment ב-Render.")
            print("3. הוסף משתנה חדש בשם TELEGRAM_CODE עם הקוד שקיבלת.")
            print("4. לחץ על Deploy -> Clear Cache and Deploy.")
            print("========================================")
            await client.send_code_request(PHONE_NUMBER)
            return
        else:
            try:
                await client.sign_in(PHONE_NUMBER, TELEGRAM_CODE)
                print("✅ החשבון אומת בהצלחה!")
            except Exception as e:
                print(f"❌ אימות נכשל: {e}")
                return

    try:
        await client(JoinChannelRequest(TARGET_CHANNEL))
        print("✅ ההצטרפות הצליחה! המשתמש מופיע בערוץ.")
    except Exception as e:
        print(f"❌ נכשל: {e}")

with client:
    client.loop.run_until_complete(main())
