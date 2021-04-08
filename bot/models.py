from sqlalchemy import Column, Integer, String,Date,Text,DateTime,Boolean,TypeDecorator,Float
from sqlalchemy import create_engine
from .config import Config
import datetime
import json

engine = create_engine(Config.DATABASE_URL, echo = True,connect_args={'check_same_thread': False})

from sqlalchemy.ext.declarative import declarative_base

class Json(TypeDecorator):

    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

Base = declarative_base()



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    date = Column(Date)
    first_name= Column(String)
    last_name=Column(String)
    username = Column(String)
    is_verified=Column(Boolean)
    is_joined_airdrop=Column(Boolean)
    twitter=Column(String)
    wallet_address=Column(String)
    is_in_channel=Column(Boolean)
    is_in_group=Column(Boolean)
    balance=Column(Float)
    email=Column(String)
    referals=Column(Integer)
    active_ref=Column(Integer)
    refferd_by=Column(Integer)
    is_multiple_account=Column(Boolean,default=False)
    

    def __init__(self, chat_id, first_name,last_name,username,refferd_by=None,email=None,is_verified=False,date=datetime.date.today(),is_joined_airdrop=False,is_in_group=False,is_in_channel=False,twitter=None,wallet_address=None,balance=0,referals=0,active_ref=0):
        self.chat_id = chat_id
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        self.date=date
        self.is_verified=is_verified
        self.is_in_channel=is_in_channel
        self.is_in_group=is_in_group
        self.is_joined_airdrop=is_joined_airdrop
        self.wallet_address=wallet_address
        self.twitter=twitter
        self.referals=referals
        self.balance=balance
        self.email=email
        self.refferd_by=refferd_by
        self.active_ref=active_ref
    def __repr__(self):
        return "<id {}>".format(self.id)
    
class Admin(Base):
    __tablename__='admins'
    id=Column(Integer,primary_key=True)
    chat_id=Column(Integer)

    def __init__(self,chat_id):
        self.chat_id=chat_id

    def __repr__(self):
        return f'{self.id}'

class Emoji(Base):
    __tablename__='emojicaptcha'
    id=Column(Integer,primary_key=True)
    chat_id=Column(Integer)
    emojis=Column(Json)
    
    def __init__(self,chat_id,emojis):
        self.chat_id=chat_id
        self.emojis=emojis

    def __repr__(self):
        return f'{self.id}'
    
class Settings(Base):
    __tablename__='setting'
    id=Column(Integer,primary_key=True)
    ref_bonus=Column(Integer,default=100)
    withdrawal_limit=Column(Integer,default=1000)
    airdrop_open=Column(Boolean,default=True)
    withdraw_open=Column(Boolean,default=False)
    
class Withdraw(Base):
    __tablename__='withdraw'
    id= Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    username=Column(String(convert_unicode=True))
    amount=Column(Float)
    address=Column(String(convert_unicode=True))
    message_id=Column(String(convert_unicode=True))
    txn=Column(String(convert_unicode=True))
    status=Column(String(convert_unicode=True))
    
class IPAddress(Base):
    __tablename__='ipaddress'
    id=Column(Integer,primary_key=True)
    chat_id=Column(Integer)
    ip=Column(String)

Base.metadata.create_all(engine)