import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, Embed, ButtonStyle
from nextcord.ui import Button, View
from colorama import Fore, Back, Style
import json
from config import  COLOR_EMBED, IMAGE_LINK, NAME, EMOJI, guildID, welcome_role, ADMIN_ROLE
from itertools import cycle
from functions.YGORole import ButtonYgoRoles, ButtonUpdate
from functions.TicketFunctions import TicketButtonUpdate
from functions.GiveawayFunctions import GiveawayChack, GiftButtonUpdate

#Class Events Cog
class Ready(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	
	@commands.Cog.listener()
	async def on_message(self, message):
			guild = message.guild
			channel = self.bot.get_channel(1093890605777694721)
			
			if message.channel.id == channel.id and not message.author.bot:
				await channel.send(IMAGE_LINK["line"])
	
	#event the bot ready
	@commands.Cog.listener()
	async def on_ready(self):
		bot = self.bot

		await ButtonUpdate(bot=bot) #run func update Button ygo role
		await GiftButtonUpdate(bot=bot)
		await TicketButtonUpdate(bot=bot) #run func for update every user ticket open button
		
		print(Fore.LIGHTRED_EX + "Name: " + Fore.LIGHTMAGENTA_EX + f"{self.bot.user.display_name} " + Fore.LIGHTGREEN_EX + "Online " + Style.RESET_ALL)
		self.bot.add_view(ButtonYgoRoles())
		print(Fore.LIGHTMAGENTA_EX + "Developed by: " + Fore.LIGHTRED_EX + "YUSI" + Style.RESET_ALL)
		
		await self.bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=NAME))
		
		await self.ChackGiveaway.start() # Start func loop chack giveaway
	
	#chack giveaway s
	@tasks.loop(seconds=5)
	async def ChackGiveaway(self):
		await GiveawayChack(bot=self.bot)
	
	
def setup(bot):
	bot.add_cog(Ready(bot))