from ..markup import tg_markup,back_markup,my_markup,join_airdrop_markup,remove_markup
from .welcome import Welcome
from ...config import Config
from ..utils.user import is_user_joined,is_wallet_found,is_mail_found,is_twitter_found,sendamount
from ...models import User
from ...extensions import session
from .welcome import Welcome
import re
import requests

MESSAGE='** Complete the task and earn 1000 RPC** .🔺 Join our Telegram Group and Channels Follow us on Twitter\n\n**Note** :\n1.Click on ✅ Joined after joining.\n2.If you leave our groups or channels, your earned token will be deduct automatically'
async def JoinAirdrop(bot,message):
    await bot.edit_message_text(message.message.chat.id,message.message.message_id,MESSAGE,reply_markup=tg_markup(),parse_mode='md')
    
async def CancelAirdrop(bot,message):
    await bot.delete_messages(message.message.chat.id,message.message.message_id )
    await Welcome(bot,message.message)
    
async def JoinedAirdrop(bot,message):
    isjoined=await is_user_joined(bot,message.message)
    if isjoined is True:
        session.query(User).filter(User.chat_id==message.message.chat.id).update({User.is_in_channel:True,User.is_in_group:True})
        session.commit()
        twitter=await bot.ask(message.message.chat.id,"Follow our Twitter account and send username of your account (include '@')\n\nNote : Don't unfollow our twitter account",parse_mode='html',reply_markup=back_markup())
        if twitter.text=='🚫 Cancel':
            await Welcome(bot,message)
        else:
            if is_twitter_found(twitter.text):
                await bot.send_message(message.message.chat.id,"This username already sumbmitted",reply_markup=remove_markup())
            else:
                email= await bot.ask(message.message.chat.id,"Send you E-mail address")
                if email.text=='🚫 Cancel':
                    await Welcome(bot,message)
                else:
                    regex = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
                    if(re.search(regex, email.text)):
                        if is_mail_found(email.text):
                            await bot.send_message(message.message.chat.id,"This E-mail already submitted",reply_markup=remove_markup())
                        else:
                            address=await bot.ask(message.message.chat.id,"Send your RapidChain address",parse_mode='html',reply_markup=back_markup())
                            if address.text=='🚫 Cancel':
                                await Welcome(bot,message)
                            else:
                                if isvalidaddress(address.text) is True:
                                    if is_wallet_found(address.text):
                                        await bot.send_message(message.message.chat.id,"This address already submitted",reply_markup=remove_markup())
                                    else:
                                        session.query(User).filter(User.chat_id==message.message.chat.id).update({User.twitter:twitter.text,
                                                                                                                User.wallet_address:address.text,
                                                                                                                User.is_joined_airdrop:True,
                                                                                                                User.balance : 1000,
                                                                                                                User.email : email.text
                                                                                                                })
                                        session.commit()
                                        user=session.query(User).filter(User.chat_id==message.message.chat.id).first()
                                        if user.refferd_by is not None:
                                            session.query(User).filter(User.chat_id==user.refferd_by).update({User.balance:User.balance+100,User.active_ref:User.active_ref+1})
                                            session.commit()
                                        else:
                                            pass
                                        
                                        DATA=f"☑️ **Thanks! Your details have been submitted successfully. Congratulations, you have earned 1000 RPC Token!** 💸\n\n\nChat ID : {message.message.chat.id}\nEmail : {email.text}\nTwitter : {twitter.text}\nRPC Address : {address.text}\n\n🔗 Your unique referral link is:\nhttps://t.me/{Config.BOT_USERNAME}?start={message.message.chat.id}\n\nShare and forward the referral link and get 100 RPC for each referral!\nThey will have to join and stay until the end of the airdrop to receive the rewards! Users who cheat will be disqualified."
                                        await bot.send_message(message.message.chat.id,DATA,parse_mode='md',reply_markup=my_markup())
                                        sent=sendamount(address.text,5)
                                        await bot.send_message(message.message.chat.id,f"You just receive 5 RPC as reward for using our bot\n🆔 Txn ID : [{sent['txid']}](http://explorer.rapid-chain.com/tx/{sent['txid']})")
                                else:
                                    await bot.send_message(message.message.chat.id,'Invalid Address, Please try again',reply_markup=remove_markup())    
                    
                    else:
                        await bot.send_message(message.message.chat.id,'Invalid E-mail address, Please try again',reply_markup=remove_markup())
    else:
        await bot.answer_callback_query(message.id,"🚫 You're not in our channels or group",show_alert=True)


def isvalidaddress(address):
    url='http://144.91.91.44/api/v1/validateAddress.php'
    json={'address' : address,'api_key' : Config.WALLET_API}
    res=requests.post(url,json=json)
    r=res.json()
    return r['result']
    
    
    
