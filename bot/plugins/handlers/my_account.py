from ...models import User
from ...extensions import session
from ...config import Config
from ..utils.user import is_airdrop_open,AirdropEnd
async def MyAccount(bot,message):
    if is_airdrop_open() is True:
        user=session.query(User).filter(User.chat_id==message.chat.id).first()
        chat_id=message.chat.id
        name=message.chat.first_name
        balance=user.balance
        twitter=user.twitter
        email=user.email
        address=user.wallet_address
        referals=user.referals
        joined=user.date
        active_ref=user.active_ref
        data=f'🆔 **ID :** {chat_id}\n📛 **Name : ** {name}\n💲 **Balance : ** {balance} RPC\n🖲 **Twitter :** {twitter}\n📧 **E-Mail :** {email}\n💳 **Wallet Address : ** {address}\n👥 **Total Referrals :** {referals}\n🔖 **Active Referrals : ** {active_ref}\n🖱 **Joined :** {joined}'
        await bot.send_message(message.chat.id,data,parse_mode='md')
    else:
        await AirdropEnd(bot,message)
    
async def InviteFriends(bot,message):
    if is_airdrop_open() is True:
        data="Invite your friends and get 100 RPC when they joined our airdrop\n\nYour referal link : https://t.me/{}?start={} ".format(Config.BOT_USERNAME,message.chat.id)
        await bot.send_message(message.chat.id,data)
    else:
        await AirdropEnd(bot,message)