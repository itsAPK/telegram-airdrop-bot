from ...models import User
from ..markup import back_markup,remove_markup,admin_markup
from ..utils.user import user_data,is_admin,delete_user
from ...config import Config
from ...extensions import session
import logging

async def MailHandler(bot,message):
    if is_admin(message.chat.id) or int(Config.ADMIN_ID)==message.chat.id:
        mail_message=await bot.ask(message.chat.id,'Enter the Message',reply_markup=back_markup())
        if mail_message.text=='🚫 Cancel':
            await bot.send_message(message.chat.id,"Mailing Canceled",reply_markup=admin_markup())
            logging.info("Mailing Cancelled")
        else:
            logging.info("Mailing Started")
            users=session.query(User).all()
            for user in users :
                try:
                    await bot.send_message(user.chat_id,mail_message.text)
                    logging.info(f"Mail sending to {user.chat_id}")
                except Exception as e:
                    logging.info(f"Mail not sent to {user.chat_id} {e}")
                    delete_user(user.chat_id)
                    
            await bot.send_message(message.chat.id,'☑️Mailing finished!',reply_markup=admin_markup())
            logging.info('☑️Mailing finished!')
    else :
        await bot.send_message(message.chat.id,'*This access only for admin*',parse_mode='markdown')


