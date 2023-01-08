from glob import glob
from os.path import basename
from json import load

from discord import AutocompleteContext, OptionChoice

from .lib import getSubcommandJSON, getTimezoneJSON

class Autocomplete:
	# Image get method
	async def getImages(self, ctx: AutocompleteContext) -> list:
		return [basename(f) for f in glob("./images/*") if ctx.value in str.lower(basename(f))]
	
	# Image command get method
	async def getImageCommand(self, ctx: AutocompleteContext) -> list:
		json = getSubcommandJSON()
		return [c for c in json.keys() if ctx.value in c]

	# Image subcommand get method
	async def getImageSubcommand(self, ctx: AutocompleteContext) -> list:
		json = getSubcommandJSON()

		if ctx.command.name in json:
			return [s for s in json[ctx.command.name] if str.lower(ctx.value) in str.lower(s)]
		else:
			return []
	
	async def getTimezone(self, ctx: AutocompleteContext) -> list:
		json = getTimezoneJSON()
		
		return [
			OptionChoice(
				name = v["name"],
				value = v["name"],
				name_localizations = {
					"ja": v["description"]
				}
			) for v in json if ctx.value in v["name"]
		]