from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            KeyboardButton, ReplyKeyboardMarkup,
                            ReplyKeyboardRemove)
from ..config import Config
from ..models import Settings
from ..extensions import session

def join_airdrop_markup():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton('🪂 Join Airdorp', callback_data='joinairdrop')
    ]])


def tg_markup():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton('📢 Join Channel', url=f'http://t.me/{Config.CHANNEL_USERNAME}')
    ], [
        InlineKeyboardButton('👥 Join Group',url=f'http://t.me/{Config.GROUP_USERNAME}')
    ],
    InlineKeyboardButton('🌐 Follow us on Twitter ',url=f"https://twitter.com/Rapidchain_"),
    [
        InlineKeyboardButton('✅ Joined',callback_data='joinetg'),
        InlineKeyboardButton('🚫 Cancel',callback_data='canceltg')
    ]
    ])

def remove_markup():
        return ReplyKeyboardRemove()
    

def back_markup():
    cancel = KeyboardButton('🚫 Cancel')
    markup = ReplyKeyboardMarkup([[cancel]], resize_keyboard=True)
    return markup

def my_markup():
    return ReplyKeyboardMarkup(
        [
        [
            KeyboardButton('🔰 My Account'),
            KeyboardButton('👥 Invite Friends')
        ],
        [
            KeyboardButton("🏦 Withdraw"),
            KeyboardButton("📈 Statistics")
        ]],resize_keyboard=True)

def admin_markup():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton('👨‍🔧 Add Admin'),
                KeyboardButton('📥 Mailing'),
                KeyboardButton('⚙️ Settings')
            ],
            [
                KeyboardButton('💲 Manage Users'),
                KeyboardButton('📮 Export User Data')
            ],   
        ],resize_keyboard=True
    )

def manage_user_markup():
    add = InlineKeyboardButton(
        '➕ Add Balance', callback_data='manageuser_addbalance')
    sub = InlineKeyboardButton(
        '➖ Reduce Balance', callback_data='manageuser_reducebalance')
    markup = InlineKeyboardMarkup([[add,sub]])
    return markup

def setting_markup():
    get=session.query(Settings).first()
    if get.withdraw_open == True:
        withdraw_open=InlineKeyboardButton('🚫 Disable Withdraw',callback_data='disable_withdraw')
    else:
        withdraw_open=InlineKeyboardButton('✅ Enable Withdraw',callback_data='enable_withdraw')
    if get.airdrop_open == True:
        airdrop_open=InlineKeyboardButton('🚫 Disable Airdrop',callback_data='disable_airdrop')
    else:
        airdrop_open=InlineKeyboardButton('✅ Enable Airdrop',callback_data='enable_airdrop')
    return InlineKeyboardMarkup([
        [
        withdraw_open,airdrop_open
        ],
        [
            InlineKeyboardButton('💰 Set Withdrawal',callback_data='set_withdrawal'),
            InlineKeyboardButton('⛔️ Set Referral',callback_data='set_ref')
            
        ],
        [
            InlineKeyboardButton('🖲 Address Info',callback_data='address_details'),
            InlineKeyboardButton('📈 Bot Statistics',callback_data='bot_stats')
        ]
                            
                            ])

def confirm_markup():
    confirm=KeyboardButton(text='✅ Confirm')
    joined_=KeyboardButton(text='🚫 Cancel')
    return ReplyKeyboardMarkup([[confirm,joined_]],resize_keyboard=True)

def withdrawal_verify(chat_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('🔘 Press',url=f"http://192.168.43.62/{chat_id}")
        ]
    ]) 
    
