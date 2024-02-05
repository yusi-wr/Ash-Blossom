import nextcord
from nextcord import ButtonStyle, Embed, SlashOption, ChannelType, Interaction, application_command
from nextcord.ext import commands, application_checks
from nextcord.abc import GuildChannel
from nextcord.ui import Button, View
import os
from config import IMAGE_LINK, COLOR_EMBED, ADMIN_ROLE, GUILD_ID, NAME , Ticket_id, owner, welcome_role, EMOJI
import json
from functions.EcoFunctoin import set_items, showitems, Buy, users_items_show, ItemsUse
from functions.YGORole import ButtonUpdate, ButtonYgoRoles, savebutton, TheEmbed
from functions.Buttons import ButtonGameLinks, ButtonPage
from functions.TicketFunctions import  CreateTicket, ClearTickets
from functions.GiveawayFunctions import GiveawayStart
from functions.Json_files import userdata


def storename():
	with open("./data/store.json", "r") as f:
		data = json.load(f)
	listname = [name for name in data]
	return listname

#cog 
class SlashCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	
	#tournaments winner
	@nextcord.slash_command(name="tournament-winner", description="Congratulations to the tournament winner")
	async def TournamentsWinner(self, interaction: Interaction, name: str=SlashOption(name="tournament-name", description="Your tournament name", required=True), user: nextcord.Member=SlashOption(name="user-winner", description="the user winner this tournaments", required=True), DP: int = SlashOption(name="dp", description="DP for winner get exampel: 1000 or 2000", required=True), channel: GuildChannel=SlashOption(name="channel", description="The channel in which we will send the congratulatory message", channel_types=[ChannelType.text], required=True)):
		
		data = await userdata()
		
		data[str(user.id)]["Tournament"] += 1
		data[str(user.id)]["DP"] += DP
		with open("./data/usersdata.json", "w") as f:
			json.dump(data, f, indent=2)
		
		
		embed = nextcord.Embed(title="**Record a new victory**" ,color=COLOR_EMBED)
		embed.description = f">>> **Tournament name: `{name.capitalize()}`\nPrize: {EMOJI['DP']} `{DP}`\nRegistered tournaments: {EMOJI['Tournament']} `{data[str(user.id)]['Tournament']}`\nThanks you :)**"
		embed.set_author(name=NAME + " | Tournaments", icon_url=IMAGE_LINK["icon"])
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1180266906314346677/1200914514376409099/1_72627WNIOVjwhWkwwb4B0Q.png")
		embed.set_footer(text=f"Sended by: {interaction.user.display_name} |")
		embed.timestamp
		
		await channel.send(f"@here • {user.mention}", embed=embed)
		await interaction.response.send_message(f"**Done successfuly - send to {channel.mention}**", ephemeral=True)
		
	
	
	# give away command
	@nextcord.slash_command(name="giveaway", description="Start a your giveaways", guild_ids=GUILD_ID)
	@application_checks.has_role(ADMIN_ROLE)
	async def Giveaway(self, interaction: Interaction,
	winners: int = SlashOption(name="winners", description="Choose the number of winners: 1, 2 or 3", required=True),
	prize: str = SlashOption(name="prize", description="Prize this giveaway", required=True),
	end: str = SlashOption(name="time-end", description="Example: 1d, h1, 30m, or 10m", required=False),
	channel: GuildChannel=SlashOption(name="channel", description="channel for send this embed", required=False, channel_types=[ChannelType.text]),
	desc: str = SlashOption(name="desc", description="Description, reason, or any message", required=False),
	mention: str = SlashOption(name="mention", description="for mention user", choices=["@here", "@everyone"], required=False)
	):
		
		await GiveawayStart(interaction=interaction, winners=winners, prize=prize, end=end, channel=channel, desc=desc, mention=mention)
		
	
	
	#Slash command tickets
	@nextcord.slash_command(name="tickets", description="Create a ticket for get help", guild_ids=GUILD_ID)
	async def Tickets(self, interaction: Interaction, desc: str = SlashOption(name="description", description="The reason and reason for opening this ticket", required=False)):
		
		try:
			await CreateTicket(interaction=interaction, desc=desc)
		except ValueError as E:
			embed = nextcord.Embed(color=COLOR_EMBED)
			embed.description = "**Sorry, We have something wrong**"
			embed.add_field(name="Here", value=f"```{E}```")
			embed.set_thumbnail(IMAGE_LINK["!"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
	
	#clear tickets
	@nextcord.slash_command(name="clear-tickets", description="Delete all active tickets all at once", guild_ids=GUILD_ID)
	async def clearTickets(self, interaction: Interaction, reason: str = SlashOption(name="reason", description="The reason why all tickets are deleted", required=False)):
		
		try:
			leader = interaction.guild.get_role(ADMIN_ROLE)
			if leader in interaction.user.roles or interaction.user.id in owner:
				await ClearTickets(bot=self.bot, interacton=interaction, reason=reason)
			else:
				embed = Embed(color=COLOR_EMBED, description=f"**Sorry {interaction.user.mention}\nOnly {leader.mention} It can delete all tickets at once**")
				embed.set_thumbnail(url=IMAGE_LINK["no"])
				embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
				return await interaction.response.send_message(embed=embed)
		except ValueError as E:
			embed = nextcord.Embed(color=COLOR_EMBED)
			embed.description = "**Sorry, We have something wrong**"
			embed.add_field(name="Here", value=f"```{E}```")
			embed.set_thumbnail(IMAGE_LINK["!"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
	
	#command Use items
	@nextcord.slash_command(name="use-items", description="use your items", guild_ids=GUILD_ID)
	async def UseItems(self, interaction: Interaction, name=SlashOption(name="items", description="Select one for use it", required=True, choices=storename()) ,user: nextcord.Member=SlashOption(name="user", description="Use it on?", required=False)):
		
		try:
			await ItemsUse(interaction=interaction, name=name, user=user)
		except ValueError as E:
			embed = nextcord.Embed(color=COLOR_EMBED)
			embed.description = "**Sorry, We have something wrong**"
			embed.add_field(name="Here", value=f"```{E}```")
			embed.set_thumbnail(IMAGE_LINK["!"])
			await interaction.response.send_message(embed=embed, ephemeral=True)

	
	#command Show user items
	@nextcord.slash_command(name="items", description="Show users items", guild_ids=GUILD_ID)
	async def ShowUserItems(self, interaction: Interaction, user: nextcord.Member=SlashOption(name="user", description="Show auther user items?", required=False)):
		
		try:
			await users_items_show(interaction=interaction, user=user)
		except ValueError as E:
			embed = nextcord.Embed(color=COLOR_EMBED)
			embed.description = "**Sorry, We have something wrong**"
			embed.add_field(name="Here", value=f"```{E}```")
			embed.set_thumbnail(IMAGE_LINK["!"])
			await interaction.response.send_message(embed=embed, ephemeral=True)



	#command buy items
	@nextcord.slash_command(name="buy", description="buy items from store", guild_ids=GUILD_ID)
	async def buy(self, interaction: Interaction, items: str = SlashOption(name="name", description="items you want buy", choices=storename(), required=True), user: nextcord.Member=SlashOption(name="user", description="Buy this items for this user?", required=False)):
		
		try:
			await Buy(interaction=interaction, name=items, user=user, ep=False)
		except ValueError as E:
			embed = nextcord.Embed(color=COLOR_EMBED)
			embed.description = "**Sorry, We have something wrong**"
			embed.add_field(name="Here", value=f"```{E}```")
			embed.set_thumbnail(IMAGE_LINK["!"])
			await interaction.response.send_message(embed=embed, ephemeral=True)
	
	
	#command show items from store
	@nextcord.slash_command(name="store", description="show items from store", guild_ids=GUILD_ID)
	async def store(self, interaction: Interaction, name: str = SlashOption(name="name", description="items name?", choices=storename(), required=False)):
		
		if name:
			await showitems(interaction=interaction, name=name)
		else:
			await showitems(interaction=interaction)
		
	
	#command slash for add new items to data store
	"""@nextcord.slash_command(name="set-items", description="Set or add new items to data store", guild_ids=GUILD_ID)
	async def SetItems(self, interaction: Interaction,
   name: str = SlashOption(name="set-name", description="Add name for this item", required=True),
   price: int = SlashOption(name="prize", description="the item prize example: 200 DP just add number", required=True),
   icon: str = SlashOption(name="set-icon", description="Link icon for items", required=True),
   amount: int = SlashOption(name="amount", required=True),
   desc: str = SlashOption(name="set-desc", required=True)
   ):
   		 try:
   		 	await set_items(interaction=interaction,name=name, price=price, icon=icon, amount=amount, desc=desc)
   		 except KeyError as E:
   		 	embed = nextcord.Embed(color=COLOR_EMBED)
   		 	embed.description = "**Sorry, We have something wrong**"
   		 	embed.add_field(name="Here", value=f"```{E}```")
   		 	embed.set_thumbnail(IMAGE_LINK["!"])
   		 	await interaction.response.send_message(embed=embed, ephemeral=True)"""
		
	
	
	#button download
	@nextcord.slash_command(name="download", description="send embed ygo link in channel", guild_ids=GUILD_ID)
	async def download(self, interaction: Interaction, channel: GuildChannel=SlashOption(name="channel", description="channel for send this embed", required=True, channel_types=[ChannelType.text])):
			embed = Embed(title="**All modern yu-gi-oh games**", color=0xff1289)
			embed.description = f"**Download all modern Yu-Gi-Oh games.\nAll links in the list are official\nDownload directly from the official games website\n\nGood luck**"
			embed.set_image(url=IMAGE_LINK["download"])
			embed.set_thumbnail(url=IMAGE_LINK["icon"])
			embed.set_footer(text=f"By: {NAME} | Thanks for: Everyone")
			
			view = ButtonGameLinks()
			role_admin = interaction.guild.get_role(ADMIN_ROLE)
			send = await interaction.response.send_message(content="<a:Loading:1140403613479489606> **Your permissions are now being verified**", ephemeral=True)
			if (role_admin) in interaction.user.roles:
				line = await channel.send(file=nextcord.File("./images/line.png"))
				msg_down = await channel.send(embed=embed, view=view)
				line2 = await channel.send(file=nextcord.File("./images/line.png"))
				await send.edit(content=f"**Sent to {channel.mention} successfully**")
				await msg_down.edit("@here", embed=embed, view=view)
				await line.edit("@here", file=nextcord.File("./images/line.png"))
				await line2.edit("@here", file=nextcord.File("./images/line.png"))
			else:
				await send.edit(content=f"** Sorry only {role_admin.mention} can use it**")
		
		
	#admin embed
	@nextcord.slash_command(name="admin-embed", description="create msg embed for news or other`s", guild_ids=GUILD_ID)
	async def admin_embed(self, interaction: Interaction, title: str=SlashOption(name="title",description="your embed title or news", required=True), desc: str=SlashOption(name="description", description="your embed description", required=True), img: nextcord.Attachment = SlashOption(name="image", description="Add image in this embed", required=False),channel: GuildChannel=SlashOption(name="channel", description="channel for send this embed", required=False, channel_types=[ChannelType.text]),  Special: str=SlashOption(name="specialty-line", description="Waht is this embed message", required=False, choices=["news", "normal"]), mention=SlashOption(name="mentions", description="Mention here or everyone", required=False, choices=["everyone", "here"])):
		role_admin = interaction.guild.get_role(ADMIN_ROLE)
		
		send = await interaction.response.send_message(content="<a:Loading:1140403613479489606> **Your permissions are now being verified**", ephemeral=True)
		if (role_admin) in interaction.user.roles:
			embed = Embed(title=f"{title}", color=COLOR_EMBED)
			embed.set_thumbnail(url=IMAGE_LINK["icon"])
			embed.description=f">>> {desc}"
			embed.set_author(name=f"{NAME}", icon_url=IMAGE_LINK["bot-icon"])
			if img:
				embed.set_image(url=img)
			if mention == "everyone":
				mentions = "@everyone"
				here = "@here"
			elif mention == "here":
				mentions = "@here"
				here = "@here"
			else:
				mentions = ""
				here = ""
			if Special == "news":
				img_line1 = f"./images/news.png"
			else:
				img_line1= "./images/line.png"
			if channel:
				img_msg = await channel.send(file=nextcord.File(img_line1))
				await img_msg.edit(f"{here}", file=nextcord.File(img_line1))
				await channel.send(f"{mentions}", embed=embed)
				img_line2 = await channel.send(file=nextcord.File("./images/line.png"))
				await img_line2.edit(f"{here}", file=nextcord.File("./images/line.png"))
				await send.edit(content=f"**Sent to {channel.mention} successfully**")
			else:
				embed = Embed(title=f"{title}", color=0xff1289)
				embed.description = f"{desc}"
				embed.set_thumbnail(url=interaction.guild.avatar.url)
				await interaction.response.send_message(f"{mentions}", embed=embed)
		else:
			await send.edit(content=f"** Sorry only {role_admin.mention} can use it**")


	#Admin Send Message
	@nextcord.slash_command(name="admin-message", description="send your importent msg or news to the cahnnels", guild_ids=GUILD_ID)
	async def admin_msg(self, interaction: Interaction, msg: str = SlashOption(name="message", description="Your message or news", required=True), channel: GuildChannel = SlashOption(name="channel", description="The channel in which the news was sent", required=False, channel_types=[ChannelType.text]), mention=SlashOption(name="mentions", description="Mention Here or everyone", required=False, choices=["everyone", "here"])):
		
		if mention == "everyone":
			mentions = "@everyone"
			here = "@here"
		elif mention == "here":
			mentions = "@here"
			here = "@here"
		else:
			mentions = ""
			here = ""
		
		role_admin = interaction.guild.get_role(ADMIN_ROLE)
		
		send = await interaction.response.send_message(content="<a:Loading:1140403613479489606> **Your permissions are now being verified**", ephemeral=True)
		if (role_admin) in interaction.user.roles:
			if channel:
				img_news = await channel.send(file=nextcord.File("./images/news.png"))
				await img_news.edit(f"{here}", file=nextcord.File("./images/news.png"))
				await channel.send(f"{mentions}\n\n<:news:1181948536728862871> **__Ash Blossom News__** <:news:1181948536728862871>\n>>> {msg}")
				img_line = await channel.send(file=nextcord.File("./images/line.png"))
				await img_line.edit(f"{here}", file=nextcord.File("./images/line.png"))
				await send.edit(content=f"**Sent to {channel.mention} successfully**")
			else:
				await interaction.channel.send(f"{mentions}\n\n<:news:1181948536728862871> **__Ash Blossom News__** <:news:1181948536728862871>\n>>> {msg}")
				await send.edit(content=f"done successfully {interaction.user.mention}")
		else:
			await send.edit(content=f"** Sorry only {role_admin.mention} can use it**")
	
	#Button Roles YuGiOh
	@nextcord.slash_command(name="ygo-role", description="Send Embed Roles in the Channel", guild_ids=GUILD_ID)
	async def ygo_role(self, interaction: Interaction, channel: GuildChannel=SlashOption(name="channel", description="channel for embed roles", required=True, channel_types=[ChannelType.text])):
		
		role_admin = interaction.guild.get_role(ADMIN_ROLE)
		send = await interaction.response.send_message(content="<a:Loading:1140403613479489606> **Your permissions are now being verified**", ephemeral=True)
		view = ButtonYgoRoles()
		if (role_admin) in interaction.user.roles:
			line = await channel.send(file=nextcord.File("./images/line.png"))
			embedmsg = await channel.send(embed=TheEmbed(), view=view)
			line2 = await channel.send(file=nextcord.File("./images/line.png"))
			await savebutton(channel.id, embedmsg.id)
			await send.edit(content=f"**Successfully sent to {channel.mention}**")
			await line.edit("@here", file=nextcord.File("./images/line.png"))
			await embedmsg.edit("@here", embed=TheEmbed(), view=view)
			await line2.edit("@here", file=nextcord.File("./images/line.png"))
		else:
			await send.edit(content=f"** Sorry only {role_admin.mention} can use it**")



def setup(bot):	
	bot.add_cog(SlashCommand(bot))