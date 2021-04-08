from ..utils.user import get_emoji,delete_emoji,verified,AirdropEnd,is_airdrop_open
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            KeyboardButton, ReplyKeyboardMarkup,
                            ReplyKeyboardRemove)
from boltons import iterutils
from .welcome import Welcome

async def ValidateCaptcha(bot,message):
    if message.data=='✅' or message.data=='❌':
        pass
    else:
        all_emoji=[]
        for i in message.message.reply_markup.inline_keyboard:
            for j in i:
                all_emoji.append(j.text)
        
#reference : https://stackoverflow.com/questions/2582138/finding-and-replacing-elements-in-a-list         
        for n,i in enumerate(all_emoji):
            if message.data in get_emoji(message.message.chat.id):
                if i == message.data:
                    all_emoji[n]='✅'
            else:
                if i == message.data:
                    all_emoji[n]='❌'
    if all_emoji.count('✅') == 5:
        delete_emoji(message.message.chat.id)
        verified(message.message.chat.id)
        await bot.delete_messages(chat_id=message.message.chat.id,
                                                            message_ids=message.message.message_id)
        if is_airdrop_open() is True:
            await Welcome(bot,message.message)
        else:
            await AirdropEnd(bot,message.message)
        
    elif all_emoji.count('❌') > 1:
        delete_emoji(message.message.chat.id)
        await bot.delete_messages(chat_id=message.message.chat.id,
                                                message_ids=message.message.message_id)
        await bot.send_message(message.message.chat.id,"**🚫 Opps.! you failed to solve the captcha.Try again..!**",parse_mode='md')
        
    else:
        emoji=iterutils.chunked(all_emoji, 5)
        markup=InlineKeyboardMarkup([[InlineKeyboardButton(x,callback_data=x) for x in emoji[0]],
                                        [InlineKeyboardButton(x,callback_data=x) for x in emoji[1]],
                                        [InlineKeyboardButton(x,callback_data=x) for x in emoji[2]]])
        await bot.edit_message_reply_markup(
                                                chat_id=message.message.chat.id,
                                                message_id=message.message.message_id,
                                                reply_markup=markup)