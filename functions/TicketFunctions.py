import nextcord
from nextcord import ButtonStyle, Embed, Interaction
from nextcord.ext import commands
import json
import asyncio
from config import NAME, COLOR_EMBED, IMAGE_LINK, Ticket_id, ADMIN_ROLE
from functions.Json_files import useritems, storedata, TicketData, userdata


#Ticket Button Settings
class SettingsTicketButton(nextcord.ui.View):
	def __init__(self, the_user_id):
		super().__init__(timeout=None)
		self.user = the_user_id
	
	#Button add user`s to a tickets
	@nextcord.ui.button(label="Add user", style=ButtonStyle.green, emoji="<:join:1140401974911705118>")
	async def AddUser(self, button: nextcord.ui.Button, interaction: Interaction):
		
		user = interaction.guild.get_member(int(self.user))
		author = interaction.user
		role = interaction.guild.get_role(Ticket_id)
		leader = interaction.guild.get_role(ADMIN_ROLE)
		
		if role not in author.roles and leader not in author.roles and author.id != user.id:
			embed = Embed(color=COLOR_EMBED)
			embed.description =f"**\nOnly {leader.mention} or {role.mention}\nand {user.mention} can close this ticket**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await interaction.response.send_message(content=f"**Sorry {author.mention}**", embed=embed, ephemeral=False)
			return
		
		await interaction.response.send_modal(AddUser(channel=interaction.channel))
	
	#Button remove a user from the tickets
	@nextcord.ui.button(label="Remove user", style=ButtonStyle.red, emoji="<:leave:1140402045275353118>")
	async def RemoveUser(self, button: nextcord.ui.Button, interaction: Interaction):
		
		user = interaction.guild.get_member(int(self.user))
		author = interaction.user
		role = interaction.guild.get_role(Ticket_id)
		leader = interaction.guild.get_role(ADMIN_ROLE)
		
		if role not in author.roles and leader not in author.roles and author.id != user.id:
			embed = Embed(color=COLOR_EMBED)
			embed.description =f"**\nOnly {leader.mention} or {role.mention}\nand {user.mention} can close this ticket**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await interaction.response.send_message(content=f"**Sorry {author.mention}**", embed=embed, ephemeral=False)
			return 
		
		await interaction.response.send_modal(RemoveUser(channel=interaction.channel))
	
	#Button close a ticket
	@nextcord.ui.button(label="Close Ticket", style=ButtonStyle.red, emoji="<:close:1198372795726450870>")
	async def CloseTicket(self, button: nextcord.ui.Button, interaction: Interaction):
		
		user = interaction.guild.get_member(int(self.user))
		author = interaction.user
		Ticket = await TicketData()
		role = interaction.guild.get_role(Ticket_id)
		leader = interaction.guild.get_role(ADMIN_ROLE)
		
		msg = await interaction.response.send_message("**<a:Loading:1140403613479489606> Deleting the ticket.....**", ephemeral=True)
		
		if role not in author.roles and leader not in author.roles and author.id != user.id:
			embed = Embed(color=COLOR_EMBED)
			embed.description =f"**\nOnly {leader.mention} or {role.mention}\nand {user.mention} can close this ticket**"
			embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await msg.edit(content=f"**Sorry {author.mention}**", embed=embed)
			return
		
		del Ticket[str(user.id)]
		with open("./data/tickets.json", "w") as f:
			json.dump(Ticket, f ,indent=2)
		await msg.edit(content=f"**The ticket is deleted - successfuly**")

		if author != user:
			await user.send(f"Hi {user.mention}\nYour ticket is closed\nClosed by: {interaction.user.mention}**")
		await msg.edit("**Delete the ticket successfully**")
		await interaction.channel.delete(reason="Ticket closed")



#Func Create a ticket
async def CreateTicket(interaction: Interaction, desc: str=None):
	
	embed = Embed(color=COLOR_EMBED)
	user = interaction.user
	guild = interaction.guild
	Items = await useritems()
	store = await storedata()
	Ticket = await TicketData()
	data = await userdata()
	
	role = interaction.guild.get_role(Ticket_id)
	leaders = interaction.guild.get_role(ADMIN_ROLE)
	if desc == None:
		desc = "Non description....."
	if str(user.id) not in data:
		embed.description =f"**Sorry, your account it`s not activated\nPlease run slash command: `/verifie`**"
		embed.set_thumbnail(url=IMAGE_LINK["no"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		return await interaction.response.send_message(embed=embed)
	
	msg = await interaction.response.send_message("**<a:Loading:1140403613479489606> Verification and implementation underway......**", ephemeral=True)
	UserItems = Items[str(user.id)]
	
	if "Super-Ticket" not in UserItems and leaders not in user.roles:
		embed.description = f">>> **Sorry, you need item `Super-Ticket`for create ticket\nRun: `/store` for get it** "
		embed.set_thumbnail(url=store["Super-Ticket"]["icon"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		return await msg.edit(content=f"**{user.mention}**", embed=embed)
		
	if str(user.id) in Ticket:
		embed.description = f">>> **Sorry, you already have a ticket\nHere: <#{int(Ticket[str(user.id)]['channel_id'])}>**"
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url=IMAGE_LINK["!"])
		await msg.edit(content=f"**{user.mention}**", embed=embed)
		return
	
	embed.title = f"**__Super-Ticket • Ticket help__**"
	embed.description = f"**Hi {user.mention} welcome to your ticket\nWait same {role.mention} for help you\n\nDescription\n>>> ```{desc}```**"
	embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
	embed.set_thumbnail(url=store["Super-Ticket"]["icon"])
	embed.set_footer(text=f'By: {interaction.user.display_name}')
	
	overwrite = {
	        guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
	        user: nextcord.PermissionOverwrite(view_channel=True),
	        role: nextcord.PermissionOverwrite(view_channel=True)
	}
	category = nextcord.utils.get(guild.categories, name="Tickets")
	channel = await guild.create_text_channel(name=f"🎟️・{user.display_name}", category=category, overwrites=overwrite)
	
	meg_embed = await channel.send(f"{role.mention} • {user.mention}", embed=embed, view=SettingsTicketButton(the_user_id=user.id))
	
	if leaders not in user.roles and "Super-Ticket" in Items[str(user.id)]:
		if Items[str(user.id)]["Super-Ticket"]["amount"] == 1:
			del Items[str(user.id)]["Super-Ticket"]
		else:
			Items[str(user.id)]["Super-Ticket"]["amount"] -= 1
	
	Ticket[str(user.id)] = {}
	Ticket[str(user.id)]["channel_id"] = str(channel.id)
	Ticket[str(user.id)]["msg_id"] = str(meg_embed.id)
	with open("./data/tickets.json", "w") as f:
		json.dump(Ticket, f, indent=2)
	with open("./data/useritems.json", "w") as f:
		json.dump(Items, f, indent=2)
	
	await msg.edit(f"**Created Ticket successfuly - {channel.mention}**")



#Func for update ticket button from any ticket opned
async def TicketButtonUpdate(bot: commands.Bot):
	
	data = await TicketData()
	
	for user_id in data:
		channel_id = data[str(user_id)]["channel_id"]
		message_id = data[str(user_id)]["msg_id"]
		channel = bot.get_channel(int(channel_id))
		message = await channel.fetch_message(int(message_id))
		
		await message.edit(view=SettingsTicketButton(the_user_id=user_id))


#Func for clear & delete all user ticket
async def ClearTickets(bot: commands.Bot, interacton: Interaction, reason: str = None):
	
	data = await TicketData()
	embed = Embed(color=COLOR_EMBED)
	
	if reason == None:
		reason = "He didn't give a reason......"
	msg = await interacton.response.send_message(embed=Embed(color=COLOR_EMBED, description="**<a:Loading:1140403613479489606> Delete all tickets......**"))
	
	list_channel = []
	for user_id in data:
		list_channel.append(user_id)
	if len(list_channel) >= 1:
		for users in list_channel:
			user = interacton.guild.get_member(int(users))
			channel_id = data[str(users)]["channel_id"]
			channel = bot.get_channel(int(channel_id))
			del data[str(users)]
			await channel.delete()
			await user.send(f">>> **Hi {user.mention}\nYour ticket is closed\nClosed by: {interacton.user.mention}\nReason: ```{reason}```**")
			
		with open("./data/tickets.json", "w") as f:
			json.dump(data, f, indent=2)
		embed.description = f"**Delete `{len(list_channel)}` tickets**"
		embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1086418616561442846.png")
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		await msg.edit(embed=embed)
	else:
		embed.description = f"**<:Think:1196170601023406126> I can't find any active tickets.....\nSorry {interacton.user.mention}**"
		embed.set_thumbnail(url=IMAGE_LINK["!"])
		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		await msg.edit(embed=embed)


#class model for add user`s in tickets
class AddUser(nextcord.ui.Modal):
	def __init__(self, channel):
		super().__init__(title="Add a user to a ticket", timeout=None)
		
		self.channel = channel
		
		self.user = nextcord.ui.TextInput(
		     label="User ID",
		     min_length=2,
		     max_length=22,
		     required=True,
		     placeholder="Add one user ID you add to here"
		)
		self.add_item(self.user)
	
	async def callback(self, interacton: Interaction) -> None:
		user = interacton.guild.get_member(int(self.user.value))
		
		embed = Embed(color=COLOR_EMBED)
		if user is None:
			embed.description =f"**Please provide the required user ID**"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await interacton.response.send_message(embed=embed, ephemeral=True)
			return
		
		overwrite = nextcord.PermissionOverwrite()
		overwrite.view_channel = True
		overwrite.read_messages = True
		
		await self.channel.set_permissions(user, overwrite=overwrite)
		embed.description = f"**Added {user.mention} to this ticket\nAdded by: {interacton.user.mention}**"
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.set_thumbnail(url=IMAGE_LINK["add"])
		await interacton.response.send_message(f"{user.mention}", embed=embed)


#class model for remove user`s in tickets
class RemoveUser(nextcord.ui.Modal):
	def __init__(self, channel):
		super().__init__(title="Remove a user to a ticket", timeout=None)
		
		self.channel = channel
		
		self.user = nextcord.ui.TextInput(
		     label="User ID",
		     min_length=2,
		     max_length=22,
		     required=True,
		     placeholder="Add one user ID here to remove it"
		)
		self.add_item(self.user)
	
	async def callback(self, interacton: Interaction) -> None:
		user = interacton.guild.get_member(int(self.user.value))
		
		embed = Embed(color=COLOR_EMBED)
		if user is None:
			embed.description =f"**Please provide the required user ID**"
			embed.set_thumbnail(url=IMAGE_LINK["!"])
			await interacton.response.send_message(embed=embed, ephemeral=True)
			return
		
		overwrite = nextcord.PermissionOverwrite()
		overwrite.view_channel = False
		overwrite.read_messages = False
		
		await self.channel.set_permissions(user, overwrite=overwrite)
		embed.description = f"**Remove {user.mention} From this ticket\nRemoved by: {interacton.user.mention}**"
		embed.set_author(name="Done successfuly", icon_url=IMAGE_LINK["ok"])
		embed.set_thumbnail(url=IMAGE_LINK["remove"])
		await interacton.response.send_message(embed=embed)