from ..markup import back_markup,admin_markup,manage_user_markup
from ...models import User
from ...extensions import session
from ..utils.user import is_admin
from ...config import Config

async def ManageUser(bot,message):
    if is_admin(message.chat.id) or int(Config.ADMIN_ID)==message.chat.id:
        usermsg=await bot.ask(message.chat.id,"Send user ID or username without @",reply_markup=back_markup())
        if usermsg.text=='🚫 Cancel':
            await bot.send_message(message.chat.id,"Action cancelled",reply_markup=admin_markup())
        else:
            await bot.send_message(message.chat.id,"Getting User details",reply_markup=admin_markup())
            try:
                user=session.query(User).filter((User.chat_id==usermsg.text) | (User.username==usermsg.text)).first()
                #data=f'🆔 ID : {user.chat_id} \n🤵 Username : @{user.username}\n💰 Balance : {user.balance}\n👥 Referals : {user.referals}\n🚚 Order : {user.orders}'
                #user=session.query(User).filter(User.chat_id==message.chat.id).first()
                chat_id=message.chat.id
                name=message.chat.first_name
                balance=user.balance
                twitter=user.twitter
                email=user.email
                address=user.wallet_address
                referals=user.referals
                joined=user.date
                data=f'🆔 **ID :** {chat_id} \n📛 **Name : ** {name}\n💲 **Balance : ** {balance} RPC\n🖲 **Twitter :** {twitter}\n📧 **E-Mail :** {email}\n💳 **Wallet Address : ** {address}\n👥 **Referrals :** {referals}\n🖱 **Joined :** {joined}'
                await bot.send_message(message.chat.id,data,reply_markup=manage_user_markup())
            except Exception:
                await bot.send_message(message.chat.id,"user not found",reply_markup=admin_markup())
                session.rollback()            
async def ManageUserQuery(bot,message):
    if is_admin(message.message.chat.id) or int(Config.ADMIN_ID)==message.message.chat.id:
        """if message.data=='manageuser_trans':
            user_id=message.message.text.split(' ')[3]
            print(message.message.text.split(' '))
            m=session.query(Transaction).filter(Transaction.chat_id==user_id,Transaction.status=='Confirmed').all()
            a=''
            for i in m:
                a+=f'\n\n🆔 **Transaction ID :**{i.txn}\n💰 **Amount :** {str(i.amt)}\n⌛️ **Status :** {i.status}'
            try:
                await bot.send_message(chat_id=message.message.chat.id,text=a,parse_mode='md')
            except Exception:
                await bot.send_message(chat_id=message.message.chat.id,text="**User don't have any Deposit yet.**",parse_mode='md') """
        
        if message.data=='manageuser_addbalance':
            user_id=message.message.text.split(' ')[3]
            print(user_id)
            bal=await bot.ask(message.message.chat.id,"Send the amount")
            try:
                session.query(User).filter(User.chat_id==user_id).update({User.balance:User.balance+float(bal.text)})
                session.commit()
                await bot.send_message(message.message.chat.id,"Updated sucessfully ")
            except Exception:
                await bot.send_message(message.message.chat.id,"Something went wrong")
                
        if message.data=='manageuser_reducebalance':
            user_id=message.message.text.split(' ')[3]
            bal=await bot.ask(message.message.chat.id,"Send the amount")
            try:
                session.query(User).filter(User.chat_id==user_id).update({User.balance:User.balance-float(bal.text)})
                session.commit()
                await bot.send_message(message.message.chat.id,"Updated sucessfully ")
            except Exception:
                await bot.send_message(message.message.chat.id,"Something went wrong")
                
        