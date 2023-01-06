from .constants import Constants
from datetime import datetime
from json import load, dump

from discord import Attachment, ApplicationContext

from os.path import splitext, isfile

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

def setSubcommandJSON(data: dict) -> dict:
	with open(file="./subcommand.json", mode="w") as fp:
		dump(fp=fp, obj=data)
	
	return getSubcommandJSON()