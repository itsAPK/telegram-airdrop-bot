from ...models import User
from ...extensions import session
from ...config import Config


async def ReferralData(bot,message):
    print(message.text[7:])
    a=[]
    user_id=session.query(User).all()
    for i in user_id:
        
        a.append(i.chat_id)
    if message.chat.id in a:
        pass
    else:
        try:                       
            session.query(User).filter(User.chat_id==int(message.text[7:])).update({User.referals : User.referals+1})
            session.commit()
            q=session.query(User).filter(User.chat_id==int(message.text[7:])).one()
            await bot.send_message(q.chat_id,f"**{message.chat.first_name}** joined the bot through your referral link\n\nYour Total Referers : {q.referals}",parse_mode='md')   
        except Exception as e:
                print(e)