from ...models import User,Withdraw
from ...extensions import session
from ..utils.user import is_airdrop_open,AirdropEnd

async def Statistics(bot,message):
    if is_airdrop_open() is True:
        total_users=session.query(User).count()
        inactive_users=session.query(User).filter(User.is_joined_airdrop==False).count()
        verfied_users=session.query(User).filter(User.is_joined_airdrop==True).count()
        tokens_claimed=1000
        total_withdraw=session.query(Withdraw).all()
        for i in total_withdraw:
            tokens_claimed+=i.amt
        await bot.send_message(message.chat.id,
                           f"🔺 **Total users : ** {total_users}\n⛔️ **Inactive users : ** {inactive_users}\n✅ **Verified Users :** {verfied_users}\n💰 **Total token claims :** {tokens_claimed} RPC",
                            parse_mode='md')
    else:
        await AirdropEnd(bot,message)
    
async def AdminStatistics(bot,message):
    total_users=session.query(User).count()
    inactive_users=session.query(User).filter(User.is_joined_airdrop==False).count()
    verfied_users=session.query(User).filter(User.is_joined_airdrop==True).count()
    multiple_accounts=session.query(User).filter(User.is_multiple_account == True).count()
    tokens_claimed=0
    total_withdraw=session.query(Withdraw).all()
    for i in total_withdraw:
            tokens_claimed+=i.amt
    await bot.send_message(message.message.chat.id,
                           f"🔺 **Total users : ** {total_users}\n⛔️ **Inactive users : ** {inactive_users}\n✅ **Verified Users :** {verfied_users}\n**❗️ Duplicate Accounts : {multiple_accounts}**\n💰 **Total token claims :** {tokens_claimed}\n",
                            parse_mode='md')
    