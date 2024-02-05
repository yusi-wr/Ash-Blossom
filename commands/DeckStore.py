import nextcord
from nextcord import ButtonStyle, Embed, SlashOption, ChannelType, Interaction, application_command, Attachment
from nextcord.ext import commands, application_checks
from nextcord.abc import GuildChannel
from nextcord.ui import Button, View
import os
from config import GUILD_ID, EMOJI, ADMIN_ROLE, owner, COLOR_EMBED, NAME, IMAGE_LINK
from functions.DeckStoreFunctions import SetDeck, DeckStoreShow
from functions.Json_files import userdata
from functions.Cooldowns import CheckCooldwon, GetCooldwon


class DeckStore(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	#slash command set deck to DeckStore
	@nextcord.slash_command(name="set-deck", description="Add your deck to DeckStore", guild_ids=GUILD_ID)
	async def adddeck(self, interaction: Interaction,
	name: str = SlashOption("name", description="this deck name for store", required=True),
	price: int = SlashOption(name="price", description="this deck price = maximum: 1500 DP", required=True),
	deckFile: Attachment = SlashOption(name="deck", description="your deck file .ydk", required=True),
	image: Attachment = SlashOption(name="background", description="background for this deck its not required", required=False),
	desc: str = SlashOption(name="deck-description", description="A description of this deck or information about it", required=False)
	):
		user = interaction.user
		data = await userdata()
		embed = Embed(color=COLOR_EMBED)
		 
		if str(user.id) not in data:
			await interaction.response.send_message("**Your account not activated \n please run slash command: `/verifie` **", ephemeral=True)
			return
			
		try:
			
			cooldwon = await CheckCooldwon(command="set-deck", user=user)
			if cooldwon == True:
				await SetDeck(interaction=interaction, name=name, price=price, deckFile=deckFile, image=image, desc=desc)
			else:
				Cooltime = await GetCooldwon(command="set-deck", user=user)
				embed.description = f"**You already used this command :)\nWait for: `{Cooltime}`\nSorry and thank you ^_^**"
				embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
				embed.set_thumbnail(url=IMAGE_LINK["no"])
				await interaction.response.send_message(embed=embed)
				
		except Exception as E:
			embed.title="**Something wrong**"
			embed.description = f">>> ```{E}```"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
	
	
	#slash command show items deck store
	@nextcord.slash_command(name="deck-store", description="Show items deck store or items user", guild_ids=GUILD_ID)
	async def deckstore(self, interaction: Interaction, user: nextcord.Member = SlashOption(name="user", description="Show only decks this user", required=False)):
		
		data = await userdata()
		embed = Embed(color=COLOR_EMBED)
		if str(interaction.user.id) not in data:
			await interaction.response.send_message("**Your account not activated \n please run slash command: `/verifie` **", ephemeral=True)
			return
		try:
			await DeckStoreShow(interaction=interaction,bot=self.bot, user=user)
		except Exception as E:
			embed.title="**something wrong**"
			embed.description = f">>> ```{E}```"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
	
	
	
	
	

def setup(bot: commands.Bot):
	bot.add_cog(DeckStore(bot))