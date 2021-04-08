from ..markup import back_markup,remove_markup,admin_markup
from ..utils.user import is_admin
from ...config import Config
from ...extensions import session
from ...models import Admin
import logging

async def AddAdminHandler(bot,message):
    if int(Config.ADMIN_ID)==message.chat.id:
        try:
            add_admin=await bot.ask(message.chat.id,"Send the telegram user id of user",reply_markup=back_markup())
            if add_admin.text=='🚫 Cancel':
                await bot.send_message(message.message.chat.id,'*Cancelled*',reply_markup=admin_markup())
            else:
                session.add(Admin(chat_id=int(add_admin.text)))
                session.commit()
                await bot.send_message(message.chat.id,'Admin added sucessfuly',reply_markup=admin_markup())
        except Exception as e:
            await bot.send_message(message.chat.id,'Aww :( , Something went wrong',reply_markup=admin_markup())
    else:
        await bot.send_message(message.chat.id,'*This access only for owner*',parse_mode='markdown')