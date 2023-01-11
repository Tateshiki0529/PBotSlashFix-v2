from discord import (
	Cog, Bot, Intents, ApplicationContext, Embed, option
)
from discord.ext.commands import slash_command as command
from modules.constants import Constants
from modules.general import General
from modules.trolls import Trolls
from modules.utils import Utils
from modules.images import Images
from modules.private import Private
from modules.votes import Votes
from modules.lib import log, getHelpJSON
from modules.autocomplete import Autocomplete
from sys import argv

GID = [Constants.P_GUILD_ID]

class PBot2(Cog):
	def __init__(self, bot: Bot) -> None:
		super().__init__()
		self.bot = bot
		self.dateFormat = Constants.dateFormat
		self.token = Constants.token
		self.devToken = Constants.devToken

		self.bot.add_cog(General(bot=self.bot))
		self.bot.add_cog(Trolls(bot=self.bot))
		self.bot.add_cog(Utils(bot=self.bot))
		self.bot.add_cog(Images(bot=self.bot))
		self.bot.add_cog(Private(bot=self.bot))
		# self.bot.add_cog(Votes(bot=self.bot))
		log("All modules loaded. Starting...")
	
	@Cog.listener()
	async def on_ready(self) -> None:
		log("%s#%s: Bot is ready!" % (self.bot.user.display_name, self.bot.user.discriminator))
		return
	
	@Cog.listener()
	async def on_application_command(self, ctx: ApplicationContext) -> None:
		log("%s#%s issued: /%s" % (ctx.user.display_name, ctx.user.discriminator, ctx.command.qualified_name))
		return
	
	@Cog.listener()
	async def on_disconnect(self) -> None:
		log("Connection closed. Bot stopped.\n")
	
	# Command: /version
	@command(
		name = "version",
		description = "Botのバージョン情報を返します [Module: Core]"
	)
	async def __version(self, ctx: ApplicationContext) -> None:
		await ctx.respond("PachinkasuBotSlashFix %s" % Constants.BOT_VERSION)
		return
	
	# Command: /help [content]
	@command(
		name = "help",
		description = "ヘルプを表示します"
	)
	@option(
		name = "content",
		type = str,
		description = "詳細を表示するコマンドやモジュール名",
		required = False,
		autocomplete = Autocomplete.getHelpOption
	)
	async def __help(self, ctx: ApplicationContext, content: str = None) -> None:
		json = getHelpJSON()
		embed = Embed(title="パチンカスBot指南書")

		if content is None:
			embed.description = "サポートしているコマンド一覧:"
			for m in json:
				val: list = []
				for d in m["commands"].values():
					val.append("- %s - %s" % (d["usage"], d["description"]))
				embed.add_field(
					name = "%s (%s)" % (m["moduleName"], m["description"]),
					value = "\n".join(val),
					inline = False
				)
		await ctx.respond(embed=embed)
		return

class EmptyBot(Cog):
	def __init__(self, bot: Bot) -> None:
		super().__init__()
		self.bot = bot
		self.dateFormat = Constants.dateFormat
		self.token = Constants.token
		self.devToken = Constants.devToken

		log("Empty Bot class loaded!", Constants.LOG_WARNING)
	@Cog.listener()
	async def on_ready(self) -> None:
		log("%s#%s: EmptyBot is ready!" % (self.bot.user.display_name, self.bot.user.discriminator))
		return
	
	# Disabled Command
	@command(
		name = "disabled",
		description = "コマンドは無効化されています！ [Module: EmergencyCore]"
	)
	async def __disabled(self, ctx: ApplicationContext):
		await ctx.respond("コマンドは無効化されています！")
		return

if __name__ == "__main__":
	bot = Bot(auto_sync_commands=True, intents=Intents().all(), dev_guild_ids=GID)
	try:
		match argv[1]:
			case "dev":
				bot.add_cog(PBot2(bot=bot))
				bot.run(Constants.devToken)
			case "devreset":
				bot.add_cog(EmptyBot(bot=bot))
				bot.run(Constants.devToken)
			case "main":
				bot.add_cog(PBot2(bot=bot))
				bot.run(Constants.token)
			case "mainreset":
				bot.add_cog(EmptyBot(bot=bot))
				bot.run(Constants.token)
			case _:
				log("Unknown argument: '%s'" % argv[1], Constants.LOG_ERROR)
				exit()
	except IndexError:
		bot.add_cog(PBot2(bot=bot))
		bot.run(Constants.token)