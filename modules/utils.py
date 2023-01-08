from discord import ApplicationContext, Bot, Cog, option
from discord.ext.commands import slash_command as command
from datetime import datetime as dt, timezone as tz, timedelta as td

from .constants import Constants
from .lib import log, getTimezoneJSON
from .autocomplete import Autocomplete

GID = [Constants.P_GUILD_ID]

class Utils(Cog):
	def __init__(self, bot: Bot) -> None:
		super().__init__()
		self.bot = bot
		self.dateFormat = Constants.dateFormat
		log("Module 'Utils' loaded.")
	
	# Command: /power <base> <exp>
	@command(
		name = "power",
		description = "おい、俺の筋肉！！×2 べき乗を計算するのかい？しないのかい？どっちなんだい！ [Module: Utils]",
		guild_ids = GID
	)
	@option(
		name = "base",
		type = float,
		description = "底",
		required = True
	)
	@option(
		name = "exp",
		type = float,
		description = "べき指数",
		required = True
	)
	async def __power(self, ctx: ApplicationContext, base: float, exp: float) -> None:
		await ctx.respond("`%.2f^%.2f` の答えは `%s` ヤーッ！ ハッ！(笑顔)" % (base, exp, pow(base=base, exp=exp)))
		return
	
	# Command: /time [timezone]
	@command(
		name = "time",
		description = "時間を返します [Module: Utils]",
		guild_ids = GID
	)
	@option(
		name = "timezone",
		type = str,
		description = "タイムゾーン",
		required = False,
		autocomplete = Autocomplete.getTimezone
	)
	async def __timezone(self, ctx: ApplicationContext, timezone: str = None) -> None:
		json = getTimezoneJSON()
		tzData = None

		if timezone is None:
			tzData = {
				"name": "Asia/Tokyo",
				"description": "アジア/東京",
				"offset": {
					"hours": 9,
					"minutes": 0
				}
			}
		else:
			for v in json:
				if v["name"] == timezone:
					tzData = v
		
		if tzData is None:
			await ctx.respond("Error: 指定されたタイムゾーン `%s` は存在しません！" % timezone)
			return
		
		datetime = dt.now().astimezone(tz=tz(offset=td(hours=tzData["offset"]["hours"], minutes=tzData["offset"]["minutes"])))

		await ctx.respond("`%s (%s) (UTC%s)` の現在の日時: `%s`" % (tzData["description"], tzData["name"], "%s:%s" % ("{:+03}".format(tzData["offset"]["hours"]), "{:02}".format(abs(tzData["offset"]["minutes"]))), datetime.strftime(self.dateFormat)))
		return