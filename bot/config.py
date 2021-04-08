import os

from dotenv import load_dotenv

load_dotenv()
class Config:
    DATABASE_URL=os.environ.get('DATABASE_URL',None)
    TELEGRAM_TOKEN=os.environ.get('TELEGRAM_TOKEN',None)
    GROUP_USERNAME=os.environ.get('GROUP_USERNAME',None)
    CHANNEL_USERNAME=os.environ.get("CHANNEL_USERNAME",None)
    CHANNEL_USERNAME1=os.environ.get("CHANNEL_USERNAME",None)
    BOT_USERNAME=os.environ.get('BOT_USERNAME',None)
    TELEGRAM_APP_HASH=os.environ.get('TELEGRAM_APP_HASH',None)
    TELEGRAM_APP_ID=os.environ.get('TELEGRAM_APP_ID',None)
    BOT_NAME=os.environ.get('BOT_NAME',None)
    ADMIN_ID=os.environ.get('ADMIN_ID',None)
    ADDRESS=os.environ.get('ADDRESS',None)
    WALLET_API=os.environ.get("WALLET_API",None)
    
    if not TELEGRAM_TOKEN:
        raise ValueError('TELEGRAM BOT TOKEN not set')

    if not CHANNEL_USERNAME:
        raise ValueError('CHANNEL USERNAME not set')

    if not GROUP_USERNAME:
        raise ValueError('GROUP_USERNAME not set')

    if not BOT_USERNAME:
        raise ValueError('BOT USERNAME not set')

    if not TELEGRAM_APP_HASH:
        raise ValueError("TELEGRAM_APP_HASH not set")

    if not TELEGRAM_APP_ID:
        raise ValueError("TELEGRAM_APP_ID not set")
    
    if not BOT_NAME:
        raise ValueError("BOT NAME not set")
    
    if not ADMIN_ID:
        raise ValueError('ADMIN ID not set')