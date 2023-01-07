from os import getenv

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")
DEV_DISCORD_TOKEN = getenv("DEV_DISCORD_TOKEN")