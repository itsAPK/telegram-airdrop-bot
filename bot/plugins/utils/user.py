from ...models import User,Admin,Emoji,Settings
from sqlalchemy.sql import exists
from ...extensions import session
from ...config import Config
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import requests
from ..markup import remove_markup

import logging

logging.getLogger('message')

def user_data(message):
    
    user=session.query(User).filter(User.chat_id == message.chat.id).all()
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    chat_id = message.chat.id
    
    if first_name == None:
        first_name = 'None'
    if last_name == None:
        last_name = 'None'
    if username == None:
        username = 'None'
    if chat_id == None:
        chat_id = 'None'
    
    if not len(user):
        if message.text[7:]=='':
            session.add(User(chat_id=message.chat.id,username=username,first_name=first_name,last_name=last_name,refferd_by=None))
            session.commit()
        else:
            session.add(User(chat_id=message.chat.id,username=username,first_name=first_name,last_name=last_name,refferd_by=int(message.text[7:])))
            session.commit()
        logging.info('New User : chat_id {} username {}'.format(chat_id,username))
    if len(user):
        session.query(User).filter(User.chat_id == message.from_user.id).update({User.first_name:first_name,User.last_name:last_name,User.username:username},synchronize_session='fetch')
        session.commit()

def is_wallet_found(wallet):
    wallets=session.query(User).filter(User.wallet_address==wallet)
    return session.query(wallets.exists()).scalar()

def is_twitter_found(twitter):
    twitters=session.query(User).filter(User.twitter==twitter)
    return session.query(twitters.exists()).scalar()

def delete_user(chat_id):
    session.query(User).filter(User.chat_id==chat_id).delete()
    session.commit()

def is_mail_found(mail):
    mails=session.query(User).filter(User.email==mail)
    return session.query(mails.exists()).scalar()

def is_admin(chat_id):
    admin=session.query(Admin).filter(Admin.chat_id==chat_id)
    return session.query(admin.exists()).scalar()

def is_verified(chat_id):
    verify=session.query(User).filter(User.chat_id==chat_id).one()
    return verify.is_verified


def verified(chat_id):
    session.query(User).filter(User.chat_id==chat_id).update({User.is_verified:True})
    session.commit()
    
def save_emoji(chat_id,emoji):
    session.add(Emoji(chat_id=chat_id,emojis=emoji))
    session.commit()
    
def get_emoji(chat_id):
    emoji=session.query(Emoji).filter(Emoji.chat_id==chat_id).first()
    return emoji.emojis

def delete_emoji(chat_id):
    session.query(Emoji).filter(Emoji.chat_id==chat_id).delete()
    session.commit()
    
async def is_user_joined(bot,message):
    status=['creator', 'administrator', 'member']
    try:
        chanl=await bot.get_chat_member(Config.CHANNEL_USERNAME,message.chat.id)
        grp=await bot.get_chat_member(Config.GROUP_USERNAME,message.chat.id)
        if chanl.status in status and grp.status in status:
            return True
            
        else :
            return False
    except Exception:
            return False
            
def is_user_join_airdrop(chat_id):
    verify=session.query(User).filter(User.chat_id==chat_id).one()
    return verify.is_joined_airdrop

def sendamount(address,amount):
    url='http://144.91.91.44/api/v1/sendtoaddress.php'
    json= {
    "from": Config.ADDRESS,
    "to": address,
    "amount": float(amount) ,
    "api_key": Config.ADDRESS
    }
    resp=requests.post(url,json=json)
    r=resp.json()
    return r
    
def validatewithdraw(amount,address):
    pass


def is_airdrop_open():
    settings=session.query(Settings).first()
    return settings.airdrop_open

async def AirdropEnd(bot,message):
    await bot.send_message(message.chat.id,"Airdrop is ended, please stay in touch here @RapidChain for next round",reply_markup=remove_markup())