from datetime import datetime
from json import dump, load

from discord import ApplicationContext, File

from .constants import Constants

def log(text: str, level: int = Constants.LOG_INFO) -> None:
	match level:
		case Constants.LOG_INFO:
			logLevel = "INFO"
		case Constants.LOG_WARNING:
			logLevel = "WARN"
		case Constants.LOG_ERROR:
			logLevel = "ERROR"
	print("[%s] [%s] %s" % (datetime.now(Constants.TZ_JST).strftime(Constants.dateFormat), logLevel, text))
	return

def array_chunk(array: list, length: int) -> list[list]:
	output = []
	for i in range(0, len(array), length):
		output.append(array[i : i + length])
	
	return output

def getSubcommandJSON() -> dict:
	with open(file="./subcommand.json", mode="r") as fp:
		return load(fp)

def getHelpJSON() -> dict:
	with open(file="./help.json", mode="r") as fp:
		return load(fp)

def getTimezoneJSON() -> dict:
	with open(file="./timezone.json", mode="r") as fp:
		return load(fp)

def getSubcommand(cmd: str) -> list:
	json = getSubcommandJSON()
	if cmd in json:
		ret: dict = json[cmd]
		return ret.keys()
	else:
		return []

def setSubcommandJSON(data: dict) -> dict:
	with open(file="./subcommand.json", mode="w") as fp:
		dump(fp=fp, obj=data)
	
	return getSubcommandJSON()

async def imageReplySelectable(ctx: ApplicationContext, command: str, subcommand: str):
	data = getSubcommandJSON()
	list = getSubcommand(command)
	if subcommand not in list:
		await ctx.respond("Error: サブコマンドは %s から選択してください！" % ", ".join(["`%s`" % subcommand for subcommand in list]))
	else:
		await ctx.respond(file=File("./images/%s" % data[command][subcommand]["path"]))