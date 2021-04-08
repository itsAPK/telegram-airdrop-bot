
from ..markup import join_airdrop_markup,my_markup
from ...config import Config


RPC="""**What is RapidChain (RPC)?**

RapidChain is coin aimed at high functionality and improved flexibility. We want RapidChain to be able to quickly adapt to the quick pace at which the cryptocurrency ecosystem is evolving. The only way to do that is through using the most advanced blockchain technologies available. This is why RapidChain was designed by a professional team of finance capital and Forex market veterans, cryptography experts and early blockchain adopters. We all share common values such as belief in decentralized governance and disruption of fiat currency system, and the desire to push the limits of Ethereum network by exploring all the revolutionary possibilities offered by smart contracts and decentralized applications"""

async def Welcome(bot,message):
    await bot.send_message(message.chat.id,RPC,parse_mode='md',reply_markup=join_airdrop_markup())
    
async def Start(bot,message):
    data=f'Hello **{message.chat.first_name}**, Welcome to {Config.BOT_USERNAME} '
    await bot.send_message(message.chat.id,data,parse_mode='md',reply_markup=my_markup())