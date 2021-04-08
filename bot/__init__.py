from pyrogram import Client,filters
from pyromod import listen
from .config import Config
import logging
import datetime
from pyrogram.handlers import MessageHandler,CallbackQueryHandler
from .plugins.handlers.start import StartHandler
from .plugins.handlers.validate_captcha import ValidateCaptcha
from .plugins.handlers.join_airdrop import (JoinAirdrop,JoinedAirdrop,CancelAirdrop)
from .plugins.handlers.stats import Statistics,AdminStatistics
from .plugins.handlers.my_account import MyAccount,InviteFriends
from .plugins.handlers.admin import AdminHandler
from .plugins.handlers.add_admin import AddAdminHandler
from .plugins.handlers.mail import MailHandler
from .plugins.handlers.manage_users import ManageUser,ManageUserQuery
from .plugins.handlers.export_user_data import ExportData
from .plugins.handlers.settings import AdminSetting,EnableWithdraw,EnableAirdrop,DisableWithdraw,DisableAirdrop,SetRefBonus,SetWithdrawal
from .plugins.handlers.withdraw import AddressDetails,Withdrawal


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

bot=Client('bot',api_id=Config.TELEGRAM_APP_ID,api_hash=Config.TELEGRAM_APP_HASH,bot_token=Config.TELEGRAM_TOKEN)

bot.add_handler(MessageHandler(StartHandler,filters.command(['start'])))
bot.add_handler(CallbackQueryHandler(ValidateCaptcha,filters.regex(r'[^\w\s,]')))
bot.add_handler(CallbackQueryHandler(JoinAirdrop,filters.regex('^joinairdrop$')))
bot.add_handler(CallbackQueryHandler(JoinedAirdrop,filters.regex('^joinetg$')))
bot.add_handler(CallbackQueryHandler(CancelAirdrop,filters.regex('^canceltg$')))
bot.add_handler(MessageHandler(Statistics,filters.regex('^📈 Statistics$')))
bot.add_handler(MessageHandler(MyAccount,filters.regex('^🔰 My Account$')))
bot.add_handler(MessageHandler(InviteFriends,filters.regex('^👥 Invite Friends$')))
bot.add_handler(MessageHandler(AdminHandler,filters.command(['admin_start'])))
bot.add_handler(MessageHandler(AddAdminHandler,filters.regex('^👨‍🔧 Add Admin$')))
bot.add_handler(MessageHandler(MailHandler,filters.regex('^📥 Mailing$')))
bot.add_handler(MessageHandler(ManageUser,filters.regex('^💲 Manage Users$')))
bot.add_handler(CallbackQueryHandler(ManageUserQuery,filters.regex('manageuser')))
bot.add_handler(MessageHandler(ExportData,filters.regex('^📮 Export User Data$')))
bot.add_handler(MessageHandler(AdminSetting,filters.regex('^⚙️ Settings$')))
bot.add_handler(CallbackQueryHandler(SetRefBonus,filters.regex('^set_ref$')))
bot.add_handler(CallbackQueryHandler(SetWithdrawal,filters.regex('^set_withdrawal$')))
bot.add_handler(CallbackQueryHandler(EnableAirdrop,filters.regex('^enable_airdrop$')))
bot.add_handler(CallbackQueryHandler(EnableWithdraw,filters.regex('^enable_withdraw$')))
bot.add_handler(CallbackQueryHandler(DisableAirdrop,filters.regex('^disable_airdrop$')))
bot.add_handler(CallbackQueryHandler(DisableWithdraw,filters.regex('^disable_withdraw$')))
bot.add_handler(CallbackQueryHandler(AddressDetails,filters.regex('^address_details$')))
bot.add_handler(CallbackQueryHandler(AdminStatistics,filters.regex('^bot_stats$')))
bot.add_handler(MessageHandler(Withdrawal,filters.regex('^🏦 Withdraw$')))