from discord import (
	Cog, Bot, ApplicationContext, Interaction, Member,
	option
)
from discord.ext.commands import slash_command as command
from .constants import Constants
from .lib import log
from math import floor
from platform import platform
from psutil import virtual_memory, cpu_count, cpu_percent, disk_usage, cpu_freq
from emoji import emojize
from asyncio import sleep as asleep

GID = [Constants.P_GUILD_ID]

class General(Cog):
	def __init__(self, bot: Bot) -> None:
		super().__init__()
		self.bot = bot
		self.dateFormat = Constants.dateFormat
		log("Module 'General' loaded.")
	
	# Command: /ping
	@command(
		name = "ping",
		description = "Ping値を返します [Module: General]",
		guild_ids = GID
	)
	async def __ping(self, ctx: ApplicationContext) -> None:
		await ctx.respond("Pong! Now latency is `%s ms`." % floor(self.bot.latency * 1000))
		return
	
	# Command: /server
	@command(
		name = "server",
		description = "サーバー情報を返します [Module: General]",
		guild_ids = GID
	)
	async def __server(self, ctx: ApplicationContext) -> None:
		CPUFrequency = cpu_freq()
		memory = virtual_memory()
		disk = disk_usage(path="/")
		await ctx.respond("```\n- Server Information -\n\n%s\nCPU   : %s GHz (%s-%s) %s/%sCore %s%%\nMemory: %s GBytes / %s GBytes (Free: %s GBytes) %s%%\nDisk  : %s GBytes / %s GBytes (Free: %s GBytes) %s%%\n```" % (
			platform(),
			round(CPUFrequency.current / 1024, 1), round(CPUFrequency.min / 1024, 1), round(CPUFrequency.max / 1024, 1), cpu_count(logical=False), cpu_count(logical=True), cpu_percent(interval=1),
			round(memory.used / Constants.DIV_GBYTE, 2), round(memory.total / Constants.DIV_GBYTE, 2), round(memory.free / Constants.DIV_GBYTE, 2), memory.percent,
			round(disk.used / Constants.DIV_GBYTE, 2), round(disk.total / Constants.DIV_GBYTE, 2), round(disk.free / Constants.DIV_GBYTE, 2), disk.percent
		))
		return
	
	# Command: /restart
	@command(
		name = "restart",
		description = "Botを再起動します [Module: General]",
		guild_ids = GID
	)
	async def __restart(self, ctx: ApplicationContext) -> None:
		if ctx.user.guild_permissions.administrator:
			msg: Interaction = await ctx.respond(emojize(":wave:"))
			await asleep(3.0)
			await msg.delete_original_message()
			await self.bot.close()
		else:
			await ctx.respond("管理者以外は実行できません！")
		return
	
	# Command: /forcerestart
	@command(
		name = "forcerestart",
		description = "Botを即再起動します [Module: General]",
		guild_ids = GID
	)
	async def __forcerestart(self, ctx: ApplicationContext) -> None:
		if ctx.user.guild_permissions.administrator:
			msg: Interaction = await ctx.respond(emojize(":wave:"))
			await msg.delete_original_message()
			await self.bot.close()
		else:
			await ctx.respond("管理者以外は実行できません！")
		return
	
	# Command: /greeting
	@command(
		name = "greeting",
		description = "メンションしてあいさつします [Module: General]",
		guild_ids = GID
	)
	@option(
		name = "type",
		type = str,
		description = "挨拶のモード",
		choices = [
			"hello",
			"goodbye",
			"morning",
			"afternoon",
			"evening",
			"newyear",
			"halloween"
		],
		required = True
	)
	@option(
		name = "target",
		type = Member,
		description = "メンションするユーザー (デフォルト: 自分)",
		required = False
	)
	async def __greeting(self, ctx: ApplicationContext, type: str, target: Member = None) -> None:
		match type:
			case "hello":
				greet = "Hello"
			case "goodbye":
				greet = "Goodbye"
			case "morning":
				greet = "Good morning"
			case "afternoon":
				greet = "Good afternoon"
			case "evening":
				greet = "Good evening"
			case "newyear":
				greet = "Happy new year"
			case "halloween":
				greet = "Happy halloween"
		
		if target is None:
			target = ctx.user
		
		await ctx.respond("%s, %s!" % (greet, target.mention))
		return
	
	# 