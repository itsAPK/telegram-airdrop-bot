import requests
import re
from ...models import User,Withdraw,Settings,Admin,IPAddress
from ..markup import my_markup,back_markup,confirm_markup,setting_markup,withdrawal_verify
from ...extensions import session
from ...config import Config
from ..utils.user import sendamount




async def Withdrawal(bot,message):
        try:
            if isipexists(message.chat.id):
                user=session.query(User).filter(User.chat_id==message.chat.id).first()
                if user.is_multiple_account is False:
                    if iswithdrawopen() is True:
                        user=session.query(User).filter(User.chat_id==message.chat.id).first()
                        value = float("{}".format(user.balance))
                        string_value = "%f" % value
                        
                        if user.balance < 1000 :
                            m=f'Your Balance for payout is too small to withdraw.\n\nAvailable Balance for payout: **{string_value} RPC**\n\nMinimum withdrawal: ** 25  RPC** '
                            await bot.send_message(message.chat.id,m,parse_mode='md')
                        else:
                            data=f'Send the amount of RPC\n\nAvailable Balance for payout: **{string_value} RPC**'
                            
                            msg=await bot.ask(message.chat.id,data,parse_mode='md',reply_markup=back_markup())
                            if msg.text=='🚫 Cancel':
                                await bot.send_message(message.chat.id,"🔺 Your Withdraw Process cancelld",reply_markup=my_markup())
                            else:
                                    try:
                                        if float(msg.text) >=1000  :
                                            if float(msg.text) >=user.balance:
                                                confirm=await bot.ask(message.chat.id,f"📌 Please confirm your withdraw deatils..\n\n💰 Amount : **{msg.text}**\n📧 Address : **{user.wallet_address}**",reply_markup=confirm_markup())
                                                if confirm.text=='✅ Confirm':
                                                    sent=sendamount(address=user.wallet_address,amount=float(msg.text))
                                                    explorer_url='http://explorer.rapid-chain.com/tx/'
                                                    if sent['status'] == 200 :
                                                        data=f"✅ **Your Withdraw Sucessful**\n\n💰 Amount : **{msg.text}**\n📧 Address : **{user.wallet_address}**\n🆔 Txn ID : [{sent['txid']}]({explorer_url}{sent['txid']})"
                                                        await bot.send_message(message.chat.id,data,parse_mode='md',reply_markup=my_markup())
                                                        channel_data=f"➕ **New Withdrawal**\n▬▬▬▬▬▬▬▬▬▬▬\n\n 📧**Address:** {user.wallet_address}\n💲 **Amount:** {msg.text} RPC\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                                                        await bot.send_message(Config.CHANNEL_USERNAME,channel_data,parse_mode='md')
                                                        session.query(User).filter(User.chat_id==message.chat.id).update({User.balance:User.balance-float(msg.text)})
                                                        session.commit()
                                                        session.add(Withdraw(chat_id=message.chat.id,amt=float(msg.text),address=user.wallet_address,txn=sent['txid'],status='Confirmed',username=message.chat.user))
                                                        session.commit()
                                                    elif sent['status'] == 500:
                                                        admins=session.query(Admin).all()
                                                        await bot.send_message(Config.ADMIN_ID,"Insufficient Funds")
                                                        for admin in admins:
                                                            await bot.send_message(admin.chat_id,"Insufficient Funds.Deposit now")
                                                        await bot.send_message(message.chat.id,"Server error, Please try again later",parse_mode='md',reply_markup=my_markup())
                                                    else:
                                                        await bot.send_message(Config.ADMIN_ID,sent)
                                                        await bot.send_message(message.chat.id,"Server error, Please try again later",parse_mode='md',reply_markup=my_markup())
                                                elif confirm.text=='🚫 Cancel':
                                                    await bot.send_message(message.chat.id,"🔺 Your Withdraw Process cancelld",reply_markup=my_markup())
                                                else:
                                                    await bot.send_message(message.chat.id,"🔺 Your Withdraw Process cancelld",reply_markup=my_markup())
                                            else: 
                                                await bot.send_message(message.chat.id,"🔺 Insufficient Withdrawal amount",reply_markup=my_markup())
                                        else:
                                            await bot.send_message(message.chat.id,"🔺 Invalid RPC.\n\n<i>Note : Your withdrawal amount is must be greater than or equal to minimum withdraw</i>",reply_markup=my_markup(),parse_mode='html')
                                    except Exception:
                                        await bot.send_message(message.chat.id,"🔺 Invalid RPC..",reply_markup=my_markup()) 
                    else:
                        await bot.send_message(message.chat.id,"Withdraw is not open",reply_markup=my_markup())
                else:
                    await bot.send_message(message.chat.id,"You already joined airdrop with different account",reply_markup=my_markup())
            else:
                await bot.send_message(message.chat.id,"Please press the button below to continue\nThen click the **🏦 Withdraw** button again",parse_mode='md',reply_markup=withdrawal_verify(message.chat.id))
        except Exception:
                await bot.send_message(message.chat.id,"🔺 Invalid RPC..",reply_markup=my_markup()) 
                

async def AddressDetails(bot,message):
    url='http://144.91.91.44/api/v1/getbalance.php'
    json={
            'address' : Config.ADDRESS,
            'api_key' : Config.WALLET_API
        }
    resp=requests.post(url,json=json).json()
    print(resp)
    if resp['status'] == 200:
        await bot.edit_message_text(message.message.chat.id,message.message.message_id,f"Address : `{Config.ADDRESS}`\nBalance : `{resp['balance']}`",parse_mode='md',reply_markup=setting_markup())
    elif resp['status']==  500:
        await bot.edit_message_text(message.message.chat.id,message.message.message_id,f"Server Busy")
        
        
def iswithdrawopen():
    db=session.query(Settings).filter(Settings.id==1).first()
    return db.withdraw_open

def isipexists(chat_id):
    ip=session.query(IPAddress).filter(IPAddress.chat_id==chat_id)
    return session.query(ip.exists()).scalar()