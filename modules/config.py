from dotenv import load_dotenv
from os import getenv
load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")
DEV_DISCORD_TOKEN = getenv("DEV_DISCORD_TOKEN")