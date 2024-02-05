import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Embed, ButtonStyle
from nextcord.ui import View, Button
import json
from random import randint, choice
from config import NAME, EMOJI, COLOR_EMBED, ADMIN_ROLE, owner, IMAGE_LINK
from .Json_files import userdata, DeckStore
import time as pyTime


#Object button deck store
class ButtonStore(nextcord.ui.View):
	def __init__(self, names, embeds, user: nextcord.Member, bot: commands.Bot, msg):
		super().__init__(timeout=300)
		self.user = user
		self.names = names
		self.page = 0
		self.embeds = embeds
		self.lens = len(self.embeds)
		self.bot = bot
		self.message = msg
	
	async def on_timeout(self):
	    for child in self.children:
	       child.disabled = True
	    await self.message.edit(view=self)
	
	@nextcord.ui.button(label="Buy", style=ButtonStyle.green, emoji="<:shopping:1196406209314562088>")
	async def buy(self, button: nextcord.ui.Button, interaction: Interaction):
		
		if interaction.user != self.user:
			 await interaction.response.send_message(f"**Sorry this for {self.user.mention}\nRun slash command: `/deck-store` for you**", ephemeral=True)
			 return
			
		try:
			await BuyDeck(interaction=interaction, name=self.names[self.page], bot=self.bot)
			
		except Exception as E:
			embed = Embed(color=COLOR_EMBED, title="**something wrong**")
			embed.description = f">>> ```{E}```"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed, ephemeral=True)

	@nextcord.ui.button(style=ButtonStyle.gray, emoji="<:page_left:1196122484567711755>1")
	async def backward(self, button: nextcord.ui.Button, interaction: Interaction):
		
		if interaction.user != self.user:
			await interaction.response.send_message(f"**Sorry this for {self.user.mention}\nRun slash command: `/deck-store` for you**", ephemeral=True)
			return
			
		if self.page == 0:
			self.page = self.lens
		else:
			self.page -= 1
		await interaction.response.edit_message(embed=self.embeds[self.page])
	
	@nextcord.ui.button(style=ButtonStyle.gray, emoji="<:page_right:1196122516360548605>")
	async def forward(self, button: nextcord.ui.Button, interaction: Interaction):
		
		if interaction.user != self.user:
			 await interaction.response.send_message(f"**Sorry this for {self.user.mention}\nRun slash command: `/deck-store` for you**", ephemeral=True)
			 return
		
		if self.page == self.lens:
			self.page = 0
		else:
			self.page += 1
		await interaction.response.edit_message(embed=self.embeds[self.page])
	
	@nextcord.ui.button(label = "Delete", style = ButtonStyle.red, emoji = "<:delete:1144665566011994165>", custom_id="delete")
	async def Delete(self, button: nextcord.ui.Button, interaction: Interaction):
		Admin = interaction.guild.get_role(ADMIN_ROLE)
		Confirme = Button(label="confirm", style=ButtonStyle.green, emoji="<:correct:1140244198566670426>")
		if Admin not in interaction.user.roles and interaction.user.id not in owner:
			interaction.response.send_message(embed=Embed(description=f"**Sorry only {Admin.mention} or owner can delete it :(**", color=COLOR_EMBED))
			return
			
		embedconfirm = Embed(description=f"**Are you really sure you want to delete this deck?\nIf yes, click the confirm button. else Hide this message**", color=COLOR_EMBED)
		embedconfirm.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
		embedconfirm.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
		
		async def ConfirmCallback(interaction: Interaction):
			
			embed = Embed(color=COLOR_EMBED)
			Store = await DeckStore()
			data = await userdata()
			
			if self.names[self.page] not in Store:
				embed.description = f"**Actually this deck is delete**"
				embed.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
				embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
				await interaction.response.send_message(embed=embed, ephemeral=True)
				return
			
			DeckOwner = await self.bot.fetch_user(int(Store[self.names[self.page]]["userID"]))
			Price = Store[self.names[self.page]]["price"]
			Compensation = Price  + randint(30, 100)
			
			embed.title = "**the deck is deleted**"
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.description = f"**Compensation: {EMOJI['DP']} `{Compensation}`\nUploded by: {DeckOwner.mention}**"
			
			await interaction.response.send_message(embed=embed, ephemeral=True)
			
			OwnerSend = Embed(title="**Your deck delete form DeckStore**", color=COLOR_EMBED)
			OwnerSend.description = f"**Name: {self.names[self.page].replace('-', ' ')}\nDeleted by: {interaction.user.mention}\nDeck Price: {EMOJI['DP']} `{Price}`\nCompensation: {EMOJI['DP']} `{Compensation}`\nReason: ```The reason may be either a report to the administrator. Or discovering something in the deck```**"
			OwnerSend.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
			OwnerSend.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
			
			await DeckOwner.send(f"{DeckOwner.mention}",embed=OwnerSend)
			
			data[str(DeckOwner.id)]["DP"] += Compensation	
			del Store[self.names[self.page]]
			with open("./data/deckstore.json", "w") as f:
				json.dump(Store, f, indent=2)
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
		
		Confirme.callback = ConfirmCallback
		view = View()
		view.add_item(Confirme)
		
		await interaction.response.send_message(embed=embedconfirm, view=view, ephemeral=True)

class ButtonStoreBuy(nextcord.ui.View):
	def __init__(self, name, user: nextcord.Member, bot: commands.Bot, msg):
		super().__init__(timeout=50)
		self.user = user
		self.bot = bot
		self.name = name
		self.message = msg
	
	async def on_timeout(self):
	    for child in self.children:
	       child.disabled = True
	    await self.message.edit(view=self)
	
	@nextcord.ui.button(label="Buy", style=ButtonStyle.green, emoji="<:shopping:1196406209314562088>")
	async def buy(self, button: nextcord.ui.Button, interaction: Interaction):
		
		if interaction.user != self.user:
			 await interaction.response.send_message(f"**Sorry this for {self.user.mention}\nRun slash command: `/deck-store` for you**", ephemeral=True)
			 return
			
		try:
			await BuyDeck(interaction=interaction, name=self.name, bot=self.bot)
			
		except Exception as E:
			embed = Embed(color=COLOR_EMBED, title="**something wrong**")
			embed.description = f">>> ```{E}```"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
	
	@nextcord.ui.button(label = "Delete", style = ButtonStyle.red, emoji = "<:delete:1144665566011994165>", custom_id="delete")
	async def Delete(self, button: nextcord.ui.Button, interaction: Interaction):
		
		Confirme = Button(label="confirm", style=ButtonStyle.green, emoji="<:correct:1140244198566670426>")
		
		Admin = interaction.guild.get_role(ADMIN_ROLE)
		if Admin not in interaction.user.roles and interaction.user.id not in owner:
			interaction.response.send_message(embed=Embed(description=f"**Sorry only {Admin.mention} or owner can delete it :(**", color=COLOR_EMBED))
			return
		embedconfirm = Embed(description=f"**Are you really sure you want to delete this deck?\nIf yes, click the confirm button. else Hide this message**", color=COLOR_EMBED)
		embedconfirm.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
		embedconfirm.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
		
		async def ConfirmCallback(interaction: Interaction):
			
			embed = Embed(color=COLOR_EMBED)
			Store = await DeckStore()
			data = await userdata()
			
			if self.name not in Store:
				embed.description = f"**Actually this deck is delete**"
				embed.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
				embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
				await interaction.response.send_message(embed=embed, ephemeral=True)
				return
			
			DeckOwner = await self.bot.fetch_user(int(Store[self.name]["userID"]))
			Price = Store[self.name]["price"]
			Compensation = Price  + randint(30, 100)
			
			embed.title = "**the deck is deleted**"
			embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
			embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
			embed.description = f"**Compensation: {EMOJI['DP']} `{Compensation}`\nUploded by: {DeckOwner.mention}**"
			
			await interaction.response.send_message(embed=embed, ephemeral=True)
			
			OwnerSend = Embed(title="**Your deck delete form DeckStore**", color=COLOR_EMBED)
			OwnerSend.description = f"**Name: {self.name.replace('-', ' ')}\nDeleted by: {interaction.user.mention}\nDeck Price: {EMOJI['DP']} `{Price}`\nCompensation: {EMOJI['DP']} `{Compensation}`\nReason: ```The reason may be either a report to the administrator. Or discovering something in the deck```**"
			OwnerSend.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
			OwnerSend.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
			
			await DeckOwner.send(f"{DeckOwner.mention}",embed=OwnerSend)
			
			data[str(DeckOwner.id)]["DP"] += Compensation	
			del Store[self.name]
			with open("./data/deckstore.json", "w") as f:
				json.dump(Store, f, indent=2)
			with open("./data/usersdata.json", "w") as f:
				json.dump(data, f, indent=2)
		
		Confirme.callback = ConfirmCallback
		view = View()
		view.add_item(Confirme)
		
		await interaction.response.send_message(embed=embedconfirm, view=view, ephemeral=True)

# user set deck in the store
async def SetDeck(interaction: Interaction, name: str, price: int, deckFile: str, image: str=None, desc: str =None):
	
	deckStore = await DeckStore()
	data = await userdata()
	user = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if data[str(user.id)]["DP"] < price:
		embed.description = f"**You don't have > {EMOJI['DP']} `{price:,}`**"
		embed.set_thumbnail(url=IMAGE_LINK["!"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif price > 1500:
		embed.description = f"**Price maximum: {EMOJI['DP']} `1500`**"
		embed.set_thumbnail(url=IMAGE_LINK["!"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	Price = price + randint(30, 100)
	Amount = 10
	Name = name.replace(" ", "-")
	
	if desc == None:
		desc = "Non description......"
	if image == None:
		image = "https://cdn.discordapp.com/attachments/1180266906314346677/1199754997571801108/Picsart_24-01-24_16-37-23-702.png"
	
	if Name in deckStore:
		embed.description = f"**Hi {user.mention}\nChange your deck name\nBecause this `{name}` name,\nActually in databese deck store **"
		embed.set_thumbnail(url=IMAGE_LINK["!"])
		embed.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	elif str(user.id) not in data:
		embed.description = f"**Hi {user.mention}\nYour account is not activated\nrun slash command: `/verifie`**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	
	deckStore[Name] = {}
	deckStore[Name]["userID"] = str(user.id)
	deckStore[Name]["price"] = Price
	deckStore[Name]["desc"] = desc
	deckStore[Name]["image"] = str(image)
	deckStore[Name]["amount"] = Amount
	deckStore[Name]["deckLink"] = str(deckFile)
	data[str(user.id)]["DP"] -= price
	with open("./data/deckstore.json", "w") as f:
		json.dump(deckStore, f, indent=2)
	with open("./data/usersdata.json", "w") as f:
		json.dump(data, f, indent=2)
	
	embed.title = "**New deck added to store**"
	embed.description =f"**Name: {name}\nUpload By: {user.mention}\nPrice: {EMOJI['DP']} `{Price:,}`\nAmount: {Amount}\n\nDescription\n>>> ```{desc}```**"
	embed.set_image(url=image)
	embed.set_author(name=NAME +" | Deck store", icon_url=IMAGE_LINK["icon"])
	embed.set_thumbnail(url=IMAGE_LINK["ok"])
	await interaction.response.send_message(embed=embed)

#func buy decks
async def BuyDeck(interaction: Interaction, name: str, bot: commands.Bot):
	
	Store = await DeckStore()
	data = await userdata()
	user = interaction.user
	embed = Embed(color=COLOR_EMBED)
	
	if name in Store:
		Deck = Store[name]
	else:
		await interaction.response.send_message(f"**I can't find `{name.replace('-', ' ').strip()}` in deck store\nOr the quantity has run out**", ephemeral=True)
		return
	if Deck["userID"] == str(user.id):
		await interaction.response.send_message("**Sorry, You can't buy your own deck. Someone else should buy it**", ephemeral=True)
		return

	userData = data[str(user.id)]
	
	if userData["DP"] < Deck["price"]:
		embed.title = "**Sorry, you can't buy this deck**"
		embed.description = f"**Your DP is: {EMOJI['DP']} `{userData['DP']:,}`\n**"
		embed.set_thumbnail(url=IMAGE_LINK["!"])
		embed.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	DeckOwner = await bot.fetch_user(int(Deck["userID"]))
	DeckLink = Deck["deckLink"]
	DeckPrice = Deck["price"]
	DeckImage = Deck["image"]
	DeckDesc = Deck["desc"]
	DeckName = name.replace("-", " ").strip()
	DPOwnerGet = DeckPrice + randint(10, 50)
	
	if Deck["amount"] == 1:
		del Store[name]
		await DeckOwner.send(f">>> **This deck is out of stock from your list\nDeck Name: ```{DeckName}```\n{DeckOwner.mention}**", delete_after=120)
		Amount = 0
	else:
		Store[name]["amount"] -= 1
		Amount = Store[name]["amount"] if Store[name] else 0
	
	data[str(user.id)]["DP"] -= DeckPrice
	data[str(DeckOwner.id)]["DP"] += DPOwnerGet
	
	
	Download = Button(label="Download", style=ButtonStyle.link, emoji="<:DOWNLOAD:1199788530075975792>", url=f"{DeckLink.split('?')[0]}")
	view = View()
	view.add_item(Download)
	
	embed.title = "**You purchased this deck**"
	embed.description = f">>> **Name: {DeckName}\nUploded by: {DeckOwner.mention}\nPrice: {EMOJI['DP']} {DeckPrice:,}**"
	embed.add_field(name="**Description**", value=f">>> ```{DeckDesc}```")
	embed.set_image(url=DeckImage)
	embed.set_author(name=NAME + " | Deck store")
	embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
	
	await user.send(f">>> {user.mention}\n**Delete message after.... <t:{int(pyTime.time()+100)}:R> **", embed=embed, view=view,delete_after=100)
	
	OwnerSend = Embed(title="**A new purchase of your deck**", color=COLOR_EMBED)
	OwnerSend.description = f"**Name: {DeckName}\nPrics: {EMOJI['DP']} `{DeckPrice:,}`\nTotal profits: {EMOJI['DP']} `{DPOwnerGet:,}`\nAmount now: {Amount}\nThe buyer: {user.mention}**"
	OwnerSend.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
	OwnerSend.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
	await DeckOwner.send(embed=OwnerSend)
	
	with open("./data/usersdata.json", "w") as f:
		json.dump(data, f, indent=2)
	with open("./data/deckstore.json", "w") as f:
		json.dump(Store, f, indent=2)
	
	reply = Embed(title="**Your purchase has been made**" , color=COLOR_EMBED)
	reply.description = f"**Send as a private message Check your direct messages**"
	reply.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
	reply.set_thumbnail(url=IMAGE_LINK["ok"])
	await interaction.response.send_message(embed=reply, ephemeral=True)


#Show deck store items
async def DeckStoreShow(interaction: Interaction, bot: commands.Bot, user: nextcord.Member = None):
	
	Store = await DeckStore()
	data = await userdata()
	Admin = interaction.guild.get_role(ADMIN_ROLE)
	embeds = []
	names = []
	embed = Embed(color=COLOR_EMBED)
	try:
		for deck in Store:
			if user:
				if int(Store[deck]["userID"]) != user.id:
					continue		
				Deck = Store[deck]
				DeckOwner = await bot.fetch_user(int(Deck["userID"]))
				DeckPrice = Deck["price"]
				DeckImage = Deck["image"]
				DeckDesc = Deck["desc"]
				DeckAmount = Deck["amount"]
				DeckName = deck.replace("-", " ").strip()
				
				embed = Embed(color=COLOR_EMBED)
				embed.title = f"**{DeckName}**"
				embed.description = f"**Price: {EMOJI['DP']} `{DeckPrice:,}`\nAmount: {DeckAmount}\nUploded by: {DeckOwner.mention}**"
				embed.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
				embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
				embed.add_field(name="**Description**", value=f">>> ```{DeckDesc}```")
				embed.set_image(url=DeckImage)
				embeds.append(embed)
				names.append(deck)
			else:
				Deck = Store[deck]
				DeckOwner = await bot.fetch_user(int(Deck["userID"]))
				DeckPrice = Deck["price"]
				DeckImage = Deck["image"]
				DeckDesc = Deck["desc"]
				DeckAmount = Deck["amount"]
				DeckName = deck.replace("-", " ").strip()
				
				embed = Embed(color=COLOR_EMBED)
				embed.title = f"**{DeckName}**"
				embed.description = f"**Price: {EMOJI['DP']} `{DeckPrice:,}`\nAmount: {DeckAmount}\nUploded by: {DeckOwner.mention}**"
				embed.set_author(name=NAME + " | Deck store", icon_url=IMAGE_LINK["icon"])
				embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1036744625475563611.png")
				embed.add_field(name="**Description**", value=f">>> ```{DeckDesc}```")
				embed.set_image(url=DeckImage)
				embeds.append(embed)
				names.append(deck)
		
		if len(embeds) > 1:
			msg = await interaction.response.send_message(f"{interaction.user.mention}", embed=embeds[0])
			view = ButtonStore(embeds=embeds, names=names, user=interaction.user, bot=bot, msg=msg)
			if Admin not in interaction.user.roles:
				view.remove_item(view.Delete)
			await msg.edit(view=view)
		elif len(embeds) == 1:
			msg = await interaction.response.send_message(f"{interaction.user.mention}", embed=embeds[0])
			view=ButtonStoreBuy(name=names[0], user=interaction.user, bot=bot, msg=msg)
			if Admin not in interaction.user.roles:
				view.remove_item(view.Delete)
			await msg.edit(view=view)
		else:
			await interaction.response.send_message(f"**Sorry, i can't find any decks in DeckStore**", ephemeral=True)
	except Exception as E:
			embed.title="**something wrong**"
			embed.description = f">>> ```{E}```"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
	

			
		