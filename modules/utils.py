from discord import ApplicationContext, Bot, Cog, option
from discord.ext.commands import slash_command as command

from .constants import Constants
from .lib import log

GID = [Constants.P_GUILD_ID]

class Utils(Cog):
	def __init__(self, bot: Bot) -> None:
		super().__init__()
		self.bot = bot
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
	
	#