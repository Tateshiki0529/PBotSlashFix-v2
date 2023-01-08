from datetime import timedelta, timezone

from . import config

class Constants:
	BOT_VERSION = "v2-1.4.0"

	dateFormat = "%Y/%m/%d %H:%M:%S"
	token = config.DISCORD_TOKEN
	devToken = config.DEV_DISCORD_TOKEN

	P_GUILD_ID = 866856960674758716

	LOG_INFO = 1
	LOG_WARNING = 2
	LOG_ERROR = 3

	TZ_JST = timezone(timedelta(hours=9), "JST")

	DIV_KBYTE = 1024
	DIV_MBYTE = 1048576
	DIV_GBYTE = 1073741824