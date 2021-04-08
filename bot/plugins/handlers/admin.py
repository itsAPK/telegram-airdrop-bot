from ...config import Config
from ..utils.user import is_admin
from ..markup import admin_markup
async def AdminHandler(bot,message):
    if is_admin(message.chat.id) or int(Config.ADMIN_ID)==message.chat.id:
        await bot.send_message(message.chat.id,"✅  You logged in as admin",reply_markup=admin_markup())
    
    
    
    
    
    
    
    