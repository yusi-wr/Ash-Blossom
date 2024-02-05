from config import COLOR_EMBED, NAME, IMAGE_LINK, YGORoles
import nextcord
from nextcord import Interaction, ButtonStyle, Embed
import json



#Object Embed Button role
class TheEmbed(nextcord.Embed):
	def __init__(self):
		super().__init__()
		
		self.title="**Yu-Gi-Oh Games Roles 🐇**"
		self.color = COLOR_EMBED
		self.description = f"**Press the button that bears the name of the game. More than one role can be selected according to the game.\n\nfor download games <#1183978422221938698> thanks**"
		self.set_author(name=NAME + " | Games roles", icon_url=IMAGE_LINK["icon"])
		self.set_thumbnail(url=IMAGE_LINK["ygorole-icon"])
		self.set_image(url=IMAGE_LINK["ygo-role"])
		self.set_footer(text=f"click to add role and again for remove")
		


#Object button for YGO roles game
class ButtonYgoRoles(nextcord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	
	@nextcord.ui.button(label="EDOPro", style=ButtonStyle.grey, emoji="<:EDOPro:1180255646415859763>",custom_id=None)
	async def EDOPro(self, button: nextcord.ui.Button, interaction: Interaction):
		role = interaction.guild.get_role(int(YGORoles["EDOPro"]))
		assert isinstance(role, nextcord.Role)
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			embedremove = Embed(description=f"**The Role {role.mention} Has been romoved**", color=COLOR_EMBED)
			embedremove.set_thumbnail(url=IMAGE_LINK["remove"])
			await interaction.response.send_message(embed=embedremove, ephemeral=True)
		
		else:
			await interaction.user.add_roles(role)
			embedadded = Embed(description=f"**The Role {role.mention}  Has been Added**", color=COLOR_EMBED)
			embedadded.set_thumbnail(url=IMAGE_LINK["add"])
			await interaction.response.send_message(embed=embedadded, ephemeral=True)
	
	@nextcord.ui.button(label="YGOOmega", style=ButtonStyle.grey, emoji="<:YGOOmega:1180255822492737706>")
	async def YGOOmega(self, button: nextcord.ui.Button, interaction: Interaction):
		role = interaction.guild.get_role(int(YGORoles["YGOOmega"]))
		assert isinstance(role, nextcord.Role)
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			embedremove = Embed(description=f"**The Role {role.mention} Has been romoved**", color=COLOR_EMBED)
			embedremove.set_thumbnail(url=IMAGE_LINK["remove"])
			await interaction.response.send_message(embed=embedremove, ephemeral=True)
		
		else:
			await interaction.user.add_roles(role)
			embedadded = Embed(description=f"**The Role {role.mention}  Has been Added**", color=COLOR_EMBED)
			embedadded.set_thumbnail(url=IMAGE_LINK["add"])
			await interaction.response.send_message(embed=embedadded, ephemeral=True)
	
	@nextcord.ui.button(label="DuelNexus", style=ButtonStyle.grey, emoji="<:DuelNexus:1180256019901841448>")
	async def DuelNexus(self, button: nextcord.ui.Button, interaction: Interaction):
		role = interaction.guild.get_role(int(YGORoles["DuelNexus"]))
		assert isinstance(role, nextcord.Role)
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			embedremove = Embed(description=f"**The Role {role.mention}  Has been romoved**", color=COLOR_EMBED)
			embedremove.set_thumbnail(url=IMAGE_LINK["remove"])
			await interaction.response.send_message(embed=embedremove, ephemeral=True)
		
		else:
			await interaction.user.add_roles(role)
			embedadded = Embed(description=f"**The Role {role.mention}  Has been Added**", color=COLOR_EMBED)
			embedadded.set_thumbnail(url=IMAGE_LINK["add"])
			await interaction.response.send_message(embed=embedadded, ephemeral=True)
	
	@nextcord.ui.button(label="DuelBook", style=ButtonStyle.grey, emoji="<:DuelBook:1180256132254683156>")
	async def DuelBook(self, button: nextcord.ui.Button, interaction: Interaction):
		role = interaction.guild.get_role(int(YGORoles["DuelBook"]))
		assert isinstance(role, nextcord.Role)
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			embedremove = Embed(description=f"**The Role {role.mention} Has been romoved**", color=COLOR_EMBED)
			embedremove.set_thumbnail(url=IMAGE_LINK["remove"])
			await interaction.response.send_message(embed=embedremove, ephemeral=True)
		
		else:
			await interaction.user.add_roles(role)
			embedadded = Embed(description=f"**The Role {role.mention}  Has been Added**", color=COLOR_EMBED)
			embedadded.set_thumbnail(url=IMAGE_LINK["add"])
			await interaction.response.send_message(embed=embedadded, ephemeral=True)
		
	@nextcord.ui.button(label="DuelLinks", style=ButtonStyle.grey, emoji="<:DuelLinks:1180256206078627902>")
	async def DuelLinks(self, button: nextcord.ui.Button, interaction: Interaction):
		role = interaction.guild.get_role(int(YGORoles["Duellink"]))
		assert isinstance(role, nextcord.Role)
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			embedremove = Embed(description=f"**The Role {role.mention} Has been romoved**", color=COLOR_EMBED)
			embedremove.set_thumbnail(url=IMAGE_LINK["remove"])
			await interaction.response.send_message(embed=embedremove, ephemeral=True)
		
		else:
			await interaction.user.add_roles(role)
			embedadded = Embed(description=f"**The Role {role.mention}  Has been Added**", color=COLOR_EMBED)
			embedadded.set_thumbnail(url=IMAGE_LINK["add"])
			await interaction.response.send_message(embed=embedadded, ephemeral=True)
		
	@nextcord.ui.button(label="MasterDuel", style=ButtonStyle.grey, emoji="<:MasterDuel:1180255916579373176>")
	async def MasterDuel(self, button: nextcord.ui.Button, interaction: Interaction):
		role = interaction.guild.get_role(int(YGORoles["MasterDuel"]))
		assert isinstance(role, nextcord.Role)
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			embedremove = Embed(description=f"**The Role {role.mention} Has been romoved**", color=COLOR_EMBED)
			embedremove.set_thumbnail(url=IMAGE_LINK["remove"])
			await interaction.response.send_message(embed=embedremove, ephemeral=True)
		
		else:
			await interaction.user.add_roles(role)
			embedadded = Embed(description=f"**The Role {role.mention}  Has been Added**", color=COLOR_EMBED)
			embedadded.set_thumbnail(url=IMAGE_LINK["add"])
			await interaction.response.send_message(embed=embedadded, ephemeral=True)


#func save button operation information in case the bot is restarted
async def savebutton(channel, msg):
	with open("./data/buttons.json", "r") as f:
		data = json.load(f)
	
	data["ygorole"] = {}
	data["ygorole"]["channel-id"] = channel
	data["ygorole"]["message-id"] = msg
	with open("./data/buttons.json", "w") as f:
		json.dump(data, f, indent=2)


#func Yes, Ior u made the buttons update so that they do not stop after restarting the bot this is for Object (ButtonYgoRoles)
# from folder events to func on_ready sart this function
async def ButtonUpdate(bot):
	with open("./data/buttons.json", "r") as f:
		data = json.load(f)
	
	if "ygorole" in data:
		channel_id = data["ygorole"]["channel-id"]
		message_id = data["ygorole"]["message-id"]
		channel = bot.get_channel(int(channel_id))
		message = await channel.fetch_message(int(message_id))
		
		
		data["ygorole"]["message-id"] = message.id
		data["ygorole"]["channel-id"] = channel.id
		await message.edit(embed=TheEmbed(), view=ButtonYgoRoles())
		with open("./data/buttons.json", "w") as f:
			json.dump(data, f,indent=2)
	else:
		return