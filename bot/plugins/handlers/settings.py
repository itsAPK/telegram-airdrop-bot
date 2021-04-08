from ..markup import setting_markup,back_markup,admin_markup
from ...models import User,Settings
from ...extensions import session
from ..utils.user import is_admin
from ...config import Config


async def AdminSetting(bot,message):
    if is_admin(message.chat.id) or int(Config.ADMIN_ID)==message.chat.id:
        setting=session.query(Settings).first()
        
        data=f"**Withdraw Limit : ** {setting.withdrawal_limit}\n**Refferal Bonus :** {setting.ref_bonus}\n**Is Airdrop Opened :** {setting.airdrop_open}\n**Is Withdraw Opened :**{setting.withdraw_open}"
        await bot.send_message(message.chat.id,data,reply_markup=setting_markup(),parse_mode='md')

async def DisableWithdraw(bot,message):
    session.query(Settings).filter(Settings.id==1).update({Settings.withdraw_open:False})
    session.commit()
    setting=session.query(Settings).first()
    data=f"**Withdraw Limit : ** {setting.withdrawal_limit}\n**Refferal Bonus :** {setting.ref_bonus}\n**Is Airdrop Opened :** {setting.airdrop_open}\n**Is Withdraw Opened :**{setting.withdraw_open}"
    await bot.edit_message_text(chat_id=message.message.chat.id,message_id=message.message.message_id,text=data,parse_mode='md',reply_markup=setting_markup())

async def EnableWithdraw(bot,message):
    session.query(Settings).filter(Settings.id==1).update({Settings.withdraw_open:True})
    session.commit()
    setting=session.query(Settings).first()
    data=f"**Withdraw Limit : ** {setting.withdrawal_limit}\n**Refferal Bonus :** {setting.ref_bonus}\n**Is Airdrop Opened :** {setting.airdrop_open}\n**Is Withdraw Opened :**{setting.withdraw_open}"
    await bot.edit_message_text(chat_id=message.message.chat.id,message_id=message.message.message_id,text=data,parse_mode='md',reply_markup=setting_markup())


async def EnableAirdrop(bot,message):
    session.query(Settings).filter(Settings.id==1).update({Settings.airdrop_open:True})
    session.commit()
    setting=session.query(Settings).first()
    data=f"**Withdraw Limit : ** {setting.withdrawal_limit}\n**Refferal Bonus :** {setting.ref_bonus}\n**Is Airdrop Opened :** {setting.airdrop_open}\n**Is Withdraw Opened :**{setting.withdraw_open}"
    await bot.edit_message_text(chat_id=message.message.chat.id,message_id=message.message.message_id,text=data,parse_mode='md',reply_markup=setting_markup())


async def DisableAirdrop(bot,message):
    session.query(Settings).filter(Settings.id==1).update({Settings.airdrop_open:False})
    session.commit()
    setting=session.query(Settings).first()
    data=f"**Withdraw Limit : ** {setting.withdrawal_limit}\n**Refferal Bonus :** {setting.ref_bonus}\n**Is Airdrop Opened :** {setting.airdrop_open}\n**Is Withdraw Opened :**{setting.withdraw_open}"
    await bot.edit_message_text(chat_id=message.message.chat.id,message_id=message.message.message_id,text=data,parse_mode='md',reply_markup=setting_markup())


async def SetWithdrawal(bot,message):
    msg=await bot.ask(message.message.chat.id,"Send the amount",reply_markup=back_markup())
    if msg.text=='🚫 Cancel':
        await bot.send_message(message.message.chat.id,"Terminated",reply_markup=admin_markup())
    else:
        session.query(Settings).filter(Settings.id==1).update({Settings.withdrawal_limit:int(msg.text)})
        session.commit()
        await bot.send_message(message.message.chat.id,"Updated Sucessfully",reply_markup=admin_markup())

async def SetRefBonus(bot,message):
    msg=await bot.ask(message.message.chat.id,"Send the amount",reply_markup=back_markup())
    if msg.text=='🚫 Cancel':
        await bot.send_message(message.message.chat.id,"Terminated",reply_markup=admin_markup())
    else:
        session.query(Settings).filter(Settings.id==1).update({Settings.ref_bonus:int(msg.text)})
        session.commit()
        await bot.send_message(message.message.chat.id,"Updated Sucessfully",reply_markup=admin_markup())
