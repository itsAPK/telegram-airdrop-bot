import csv
from ...config import Config
from ..utils.user import is_admin
from ..markup import admin_markup
from ...models import User
from ...extensions import session
import time


async def ExportData(bot,message):
    if is_admin(message.chat.id) or int(Config.ADMIN_ID)==message.chat.id:
        users=session.query(User).all()
        msg=await bot.send_message(message.chat.id,"Uploading details from database to file,This may take while")
        m=msg
        with open("users.csv","w",encoding='UTF-8') as f:
            writer = csv.writer(f,delimiter=",",lineterminator="\n")
            writer.writerow(['id','name','username','is joined airdrop','twitter','email','wallet address','balance','referrals'])
            for user in users:
                if user.username:
                    username= user.username
                else:
                    continue
                if user.first_name:
                    first_name= user.first_name
                else:
                    first_name= ""
                if user.last_name:
                    last_name= user.last_name
                else:
                    last_name= ""
                name= (first_name + ' ' + last_name).strip()
                writer.writerow([user.chat_id,name,username,user.is_joined_airdrop,user.twitter,user.email,user.wallet_address,user.balance,user.referals]) 
        await bot.send_document(message.chat.id,'users.csv',progress=progress)
def progress(current, total):
    print(f"{current}-{total}")