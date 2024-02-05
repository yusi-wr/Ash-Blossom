import nextcord
from nextcord import Interaction, ButtonStyle, Embed
from .Json_files import useritems
from config import COLOR_EMBED, NAME
import asyncio
import json



#Buttons object  for Page Embeds
class ButtonPage(nextcord.ui.View):
	def __init__(self, embeds, msg):
		super().__init__(timeout=300)
		
		self.page = 0
		self.embeds = embeds
		self.lens = len(self.embeds)
		self.message = msg
	
	async def on_timeout(self):
	    for child in self.children:
	       child.disabled = True
	    await self.message.edit(view=self)
	
	@nextcord.ui.button(style=ButtonStyle.gray, emoji="<:page_left:1196122484567711755>1")
	async def backward(self, button: nextcord.ui.Button, interaction: Interaction):
		
		if self.page == 0:
			self.page = self.lens
		else:
			self.page -= 1
		await interaction.response.edit_message(embed=self.embeds[self.page])
	
	@nextcord.ui.button(style=ButtonStyle.gray, emoji="<:page_right:1196122516360548605>")
	async def forward(self, button: nextcord.ui.Button, interaction: Interaction):
		
		if self.page == self.lens:
			self.page = 0
		else:
			self.page += 1
		await interaction.response.edit_message(embed=self.embeds[self.page])


#class object Button Games Links
class ButtonGameLinks(nextcord.ui.View):
	def __init__(self):
		super().__init__(timeout=300)
		
		EDOPro = nextcord.ui.Button(label="EDOPro", style=ButtonStyle.link, emoji="<:EDOPro:1180255646415859763>", url='https://projectignis.github.io/download.html')
		
		Omega = nextcord.ui.Button(label="YGO Omega", style=ButtonStyle.link, emoji="<:YGOOmega:1180255822492737706>", url="https://omega.duelistsunite.org/")
		
		MasterDuel = nextcord.ui.Button(label="Master Duel", style=ButtonStyle.link, emoji="<:MasterDuel:1180255916579373176>", url="https://www.konami.com/yugioh/masterduel/us/en/")
		
		DuelLink = nextcord.ui.Button(label="DuelLinks", style=ButtonStyle.link, emoji="<:DuelLinks:1180256206078627902>", url="https://www.konami.com/yugioh/duel_links/en/")
		
		Nexus = nextcord.ui.Button(label="Dueling Nexus", style=ButtonStyle.link, emoji="<:DuelNexus:1180256019901841448>", url="https://duelingnexus.com/")
		
		Book = nextcord.ui.Button(label="Dueling Book", style=ButtonStyle.link, emoji="<:DuelBook:1180256132254683156>", url="https://www.duelingbook.com/")
		
		self.add_item(EDOPro)
		self.add_item(Omega)
		self.add_item(MasterDuel)
		self.add_item(DuelLink)
		self.add_item(Nexus)
		self.add_item(Book)
	
	
#Class Button for func users profiles
class ButtonFuncProfile(nextcord.ui.View):
	def __init__(self, embed_page1, embed_page2, msg,user: nextcord.Member = None):
		super().__init__(timeout=100)
		
		self.page1 = embed_page1
		self.page2 = embed_page2
		self.user = user
		self.message = msg
	
	async def on_timeout(self):
	    for child in self.children:
	       child.disabled = True
	    await self.message.edit(view=self)
	    
	#button for show any items user have
	@nextcord.ui.button(label="Items", style=ButtonStyle.grey, emoji="<:backpack5:1196125848403718175>")
	async def Items(self, button: nextcord.ui.Button, interaction: Interaction):
		user = self.user
		items = await useritems()
		get_user_items = items[str(user.id)]
		
		list_embeds = []
		for items in get_user_items:
			embed = nextcord.Embed(color=COLOR_EMBED)
			embed.title = f"**{items}**"
			embed.description = f"**\nQuantity owned: `{get_user_items[items]['amount']}`**"
			embed.add_field(name="**Description**", value=f">>> ```{get_user_items[items]['desc']}```")
			embed.set_thumbnail(url=get_user_items[items]["icon"])
			embed.set_author(name=f"Storage bag | {self.user.display_name}", icon_url="https://cdn.discordapp.com/emojis/695306067327844415.png")
			embed.set_footer(text=f"Quantity of items: {len([name for name in get_user_items])} | By: {NAME}", icon_url=self.user.avatar.url)
			list_embeds.append(embed)
		
		
		if len(list_embeds) > 1:
			msg = await interaction.response.send_message(embed=list_embeds[0], ephemeral=True)
			await msg.edit(view=ButtonPage(embeds=list_embeds, msg=msg))
		elif len(list_embeds) == 1:
			await interaction.response.send_message(f"{interaction.user.mention}", embed=embed,ephemeral=True)
		else:
			await interaction.response.send_message("**Sorry i can't find items in the data <:Think:1196170601023406126> **",ephemeral=True)
	
	#button for profile page 1
	@nextcord.ui.button(label="Page 1", style=ButtonStyle.grey, emoji="<:SY_Page:1196122570127314984>")
	async def Page1(self, button: nextcord.ui.Button, interaction: Interaction):
		await interaction.message.edit(embed=self.page1)
	
	#button for profile page 2
	@nextcord.ui.button(label="Page 2", style=ButtonStyle.grey, emoji="<:SY_Page:1196122570127314984>")
	async def Page2(self, button: nextcord.ui.Button, interaction: Interaction):
		await interaction.message.edit(embed=self.page2)