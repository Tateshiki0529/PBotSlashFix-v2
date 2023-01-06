from discord import (
	Cog, Bot, Intents, ApplicationContext
)
from discord.ext.commands import slash_command as command
from modules.constants import Constants
from modules.general import General
from modules.trolls import Trolls
from modules.utils import Utils
from modules.images import Images
from modules.private import Private
from modules.lib import log
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
		description = "Botのバージョン情報を返します [Module: Core]",
		guild_ids = GID
	)
	async def __version(self, ctx: ApplicationContext) -> None:
		await ctx.respond("PachinkasuBotSlashFix %s" % Constants.BOT_VERSION)
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
		description = "コマンドは無効化されています！ [Module: EmergencyCore]",
		guild_ids = GID
	)
	async def __disabled(self, ctx: ApplicationContext):
		await ctx.respond("コマンドは無効化されています！")
		return

if __name__ == "__main__":
	bot = Bot(auto_sync_commands=True, intents=Intents().all())
	try:
		if argv[1] == "reset":
			bot.add_cog(EmptyBot(bot=bot))
	except IndexError:
		bot.add_cog(PBot2(bot=bot))
	
	bot.run(Constants.devToken)