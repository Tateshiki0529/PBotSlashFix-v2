from glob import glob
from os.path import basename, isfile, splitext

from discord import ApplicationContext, Attachment, Bot, Cog, File, option
from discord.ext.commands import slash_command as command

from .autocomplete import Autocomplete
from .constants import Constants
from .lib import getSubcommandJSON, log, setSubcommandJSON

GID = [Constants.P_GUILD_ID]

class Images(Cog):
	def __init__(self, bot: Bot) -> None:
		super().__init__()
		self.bot = bot
		log("Module 'Images' loaded.")

	# Command: /imgview
	@command(
		name = "imgview",
		description = "画像を表示します [Module: Images]"
	)
	@option(
		name = "filename",
		type = str,
		description = "画像の名前",
		autocomplete = Autocomplete.getImages,
		required = False
	)
	async def __imgview(self, ctx: ApplicationContext, filename: str = None) -> None:
		if filename is not None and isfile("./images/%s" % filename):
			await ctx.respond(file=File("./images/%s" % filename))
		elif filename is None:
			files = glob("./images/*")
			output = "ファイル一覧:\n```\n"
			for f in files:
				if len(output) > 1900:
					output += "And more...\n```"
					await ctx.respond(output)
					return
				else:
					output += "- %s\n" % basename(f)
			if len(files) == 0:
				output += "- (No images)\n"
			output += "```"
			await ctx.respond(output)
		else:
			await ctx.respond("ファイル `%s` が存在しません！" % filename)
		return
	
	# Command: /upload <(file)> [filename]
	@command(
		name = "upload",
		description = "画像をアップロードします [Module: Images]"
	)
	@option(
		name = "file",
		type = Attachment,
		description = "アップロードする画像ファイル",
		required = True
	)
	@option(
		name = "filename",
		type = str,
		description = "保存するファイル名 (省略可)",
		required = False
	)
	async def __upload(self, ctx: ApplicationContext, file: Attachment, filename: str = None) -> None:
		await ctx.defer()

		if filename is None:
			filename = file.filename

		if file.content_type is not None:
			if "image" not in file.content_type:
				await ctx.respond("Error: 画像ファイルを送信してください！")
				return
		else:
			if "heic" or "heif" not in file.filename.lower():
				await ctx.respond("Error: 画像ファイルを送信してください！")
				return
			
		if filename is None:
			filename = file.filename
		else:
			if splitext(filename)[1] == "":
				await ctx.respond("Error: 名前を指定する場合は拡張子を含めてください！")
				return
		
		if isfile("./images/%s" % filename):
			await ctx.respond("Error: 画像 `%s` は既にアップロード済みです！" % filename)
			return

		if "heic" or "heif" in file.filename.lower():
			filename = splitext(filename)[0] + ".jpg"
			
		with open(file="./images/%s" % filename, mode="wb") as fp:
			data = await file.read()
			fp.write(data)
		
		await ctx.respond("ファイルを `%s` に保存しました！" % (filename), file=File("./images/%s" % filename))
		return

	# Command: /register <command> <subcommand> <path> [description] [(file)] [filename]
	@command(
		name = "register",
		description = "新しいサブコマンドを登録します [Module: Images]"
	)
	@option(
		name = "command",
		type = str,
		description = "追加先のコマンド名",
		autocomplete = Autocomplete.getImageCommand,
		required = True
	)
	@option(
		name = "subcommand",
		type = str,
		description = "追加先のサブコマンド名",
		required = True
	)
	@option(
		name = "path",
		type = str,
		description = "返信する画像のパス",
		autocomplete = Autocomplete.getImages,
		required = False
	)
	@option(
		name = "description",
		type = str,
		description = "画像の簡易的な説明",
		required = False
	)
	@option(
		name = "file",
		type = Attachment,
		description = "アップロードする画像ファイル",
		required = False
	)
	@option(
		name = "filename",
		type = str,
		description = "保存するファイル名 (省略可)",
		required = False
	)
	async def __register(
		self, ctx: ApplicationContext,
		command: str, subcommand: str, path: str = None,
		description: str = None, file: Attachment = None, filename: str = None
	) -> None:
		json = getSubcommandJSON()

		if command not in json:
			await ctx.respond("Error: `/%s` は追加可能なコマンドではありません！" % command)
			return
		elif subcommand in json[command]:
			await ctx.respond("Error: `/%s %s` は既に登録されています！" % (command, subcommand))
			return
		elif file is None and path is not None and not isfile("./images/%s" % path):
			await ctx.respond("Error: 画像 `%s` は存在しません！先に `/upload` でアップロードするか、`/register`の`file`引数に添付してください。" % path)
			return
		elif file is None and path is None:
			await ctx.respond("Error: 画像を添付しない場合はファイルパスを指定してください！")
			return
		else:
			if file is not None:
				if file.content_type is not None:
					if "image" not in file.content_type:
						await ctx.respond("Error: 画像ファイルを送信してください！")
						return
				else:
					if "heic" or "heif" not in file.filename.lower():
						await ctx.respond("Error: 画像ファイルを送信してください！")
						return
					
				if filename is None:
					filename = file.filename
				else:
					if splitext(filename)[1] == "":
						await ctx.respond("Error: 名前を指定する場合は拡張子を含めてください！")
						return
				
				if isfile("./images/%s" % filename):
					await ctx.respond("Error: 画像 `%s` は既にアップロード済みです！" % filename)
					return

				if "heic" or "heif" in file.filename.lower():
					filename = splitext(filename)[0] + ".jpg"
					
				with open(file="./images/%s" % filename, mode="wb") as fp:
					data = await file.read()
					fp.write(data)
				
				await ctx.respond("ファイルを `%s` に保存しました！" % (filename), file=File("./images/%s" % filename))
				sendAsResponse = False
			else:
				sendAsResponse = True
			
			json[command][subcommand] = {
				"description": description,
				"path": path
			}

			setSubcommandJSON(data=json)
			output = "コマンド `/%s %s` を登録しました！" % (command, subcommand)

		if sendAsResponse:
			await ctx.respond(output)
		else:
			await ctx.channel.send(output)
		
		return