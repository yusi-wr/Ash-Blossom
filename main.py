import nextcord
from nextcord.ext import commands, tasks
from nextcord.ui import Button, View
from nextcord import ButtonStyle, Interaction
import os
from colorama import Fore, Back, Style
import config
from functions.YGOCardsFunctions import  Update

bot = commands.Bot(command_prefix = "?", intents=nextcord.Intents.all(), case_insensitive=True, strip_after_prefix=True)


#tasks for update card after 24H
@tasks.loop(minutes=60 * 24)
async def ForUpdateCards():
	await Update()

@bot.event
async def on_ready():
	print(Fore.LIGHTGREEN_EX + "Start " + Fore.LIGHTBLUE_EX + " • " + Fore.LIGHTMAGENTA_EX + "Update Cards")
	await ForUpdateCards.start() # Start Func Update Yugioh cards






#load the cogs files commands
for filename in os.listdir("./commands"):
	if filename.endswith("py"):
		bot.load_extension(f"commands.{filename[:-3]}")
		print(Fore.LIGHTMAGENTA_EX + f"Loading" + " | " + Fore.LIGHTBLUE_EX + f"({filename[:-3]}) " + Fore.LIGHTGREEN_EX + "Ready")
print(Fore.LIGHTBLUE_EX + "-"* 20 + Style.RESET_ALL)

#load the cogs files events
for filename in os.listdir("./events"):
	if filename.endswith("py"):
		bot.load_extension(f"events.{filename[:-3]}")
		print(Fore.LIGHTMAGENTA_EX + f"Loading" + " | " + Fore.LIGHTBLUE_EX + f"({filename[:-3]}) " + Fore.LIGHTGREEN_EX + "Ready")
print(Fore.LIGHTBLUE_EX + "-" * 20 + Style.RESET_ALL)


#Bot login 
try:
	bot.run(config.TOKEN) #add your TOKEN Bot in file .env
except ValueError as E:
	print(E)
