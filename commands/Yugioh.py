import nextcord
from nextcord import ButtonStyle, Interaction, Embed, SlashOption, Message
from nextcord.ext import commands
from nextcord.ui import Button, View
from functions.YGOCardsFunctions import cards
from functions.Json_files import cardsname
from functions.Buttons import ButtonPage
from random import choice
import json
from difflib import get_close_matches as gcm
from config import GUILD_ID, COLOR_EMBED, IMAGE_LINK, NAME

cards_names = cardsname()

class Yugioh(commands.Cog):
	"""Yugioh commands"""
	def __init__(self, bot: commands.Context):
		self.bot = bot
	
	COG_EMOJI = "<:yugioh:1196124034014916668>"
	
	@commands.Cog.listener()
	async def on_message(self, message: Message):
		if message.author.bot:
			return
		
		if ("<" and ">") in message.content:
			author = message.author
			name = message.content.split("<>")
			
			card = cards(name=name)
			card.Api()
				
			embedcard = Embed(description=f"{card.Banlist()}{card.Type_Race()}{card.archetype()}{card.Raiity()}{card.Atk_def_Level_Scale()}", color=card.color())
			embedcard.set_author(icon_url=card.url_icon(), name=card.name)
			embedcard.set_thumbnail(url=card.CardsImage())
			embedcard.add_field(name="**Card Text**", value=f">>> {card.desc()}") 
			embedcard.add_field(name="**<:links:1192077374938939394> Link**", value=card.Links() + f"\n**[YGOPro Deck]({card.cards_url})**")
			embedcard.set_footer(icon_url=author.avatar.url,  text=f"ID: {card.cards_id()}")
				
			await message.reply(embed=embedcard)
	
			
	
	@commands.command(name="card", aliases=["c"])
	@commands.guild_only()
	async def card(self, ctx, *, name: str):
		"""command search cards by name"""
		
		card = cards(name=name)
		card.Api()
			
		embedcard = Embed(description=f"{card.Banlist()}{card.Type_Race()}{card.archetype()}{card.Raiity()}{card.Atk_def_Level_Scale()}", color=card.color())
		embedcard.set_author(icon_url=card.url_icon(), name=card.name)
		embedcard.set_thumbnail(url=card.CardsImage())
		embedcard.add_field(name="**Card Text**", value=f">>> {card.desc()}") 
		embedcard.add_field(name="**<:links:1192077374938939394> Link**", value=card.Links() + f"\n**[YGOPro Deck]({card.cards_url})**")
		embedcard.set_footer(icon_url=ctx.author.avatar.url,  text=f"ID: {card.cards_id()}")
			
		await ctx.reply(embed=embedcard)
		
	
	@commands.command(name="random", aliases=["r"])
	@commands.guild_only()
	async def randomcards(self, ctx: commands.Context):
		"""command get a random cards"""
		
		card = cards(name=choice(cards_names))
		card.Api()
		
		embedcard = Embed(description=f"{card.Banlist()}{card.Type_Race()}{card.archetype()}{card.Raiity()}{card.Atk_def_Level_Scale()}", color=card.color())
		embedcard.set_author(icon_url=card.url_icon(), name=card.name)
		embedcard.set_thumbnail(url=card.CardsImage())
		embedcard.add_field(name="**Card Text**", value=f">>> {card.desc()}") 
		embedcard.add_field(name="**<:links:1192077374938939394> Link**", value=card.Links() + f"\n**[YGOPro Deck]({card.cards_url})**")
		embedcard.set_footer(icon_url=ctx.author.avatar.url,  text=f"ID: {card.cards_id()}")
		
		await ctx.reply(embed=embedcard)
	
	
	@commands.command(name="art")
	@commands.guild_only()
	async def artcards(self, ctx: commands.Context, *, name: str):
		"""command get arts cards"""
		
		card = cards(name=name)
		card.Api()
			
		embedcard = Embed(color=card.color())
		embedcard.set_author(icon_url=card.url_icon(), name=card.name, url=card.cards_url)
		embedcard.set_image(url=card.CardsImage()) 
		embedcard.set_footer(icon_url=ctx.author.avatar.url,  text=f"ID: {card.cards_id()}")
			
		await ctx.reply(embed=embedcard)
	
	
	@commands.command(name="randomart", aliases=["rart"])
	@commands.guild_only()
	async def randomart(self, ctx: commands.Context):
		"""command get random arts cards"""
		
		card = cards(name=choice(cards_names))
		card.Api()
		
		embedcard = Embed(color=card.color())
		embedcard.set_author(icon_url=card.url_icon(), name=card.name, url=card.cards_url)
		embedcard.set_image(url=card.CardsImage())
		embedcard.set_footer(icon_url=ctx.author.avatar.url,  text=f"ID: {card.cards_id()}")
		
		await ctx.reply(embed=embedcard)
	
	
	@commands.command(name="pics")
	@commands.guild_only()
	async def pics(self, ctx: commands.Context, *, name: str):
		"""command get pics cards"""
		
		card = cards(name=name)
		card.Api()
			
		embedcard = Embed(color=card.color())
		embedcard.set_author(icon_url=card.url_icon(), name=card.name, url=card.cards_url)
		embedcard.set_image(url=f"https://images.ygoprodeck.com/images/cards/{card.cards_id()}.jpg") 
		embedcard.set_footer(icon_url=ctx.author.avatar.url,  text=f"ID: {card.cards_id()}")
			
		await ctx.reply(embed=embedcard)
	
	


def setup(bot):
	bot.add_cog(Yugioh(bot))