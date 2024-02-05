import  nextcord
from nextcord import Interaction, Embed, ButtonStyle
from nextcord.ext import commands, tasks
import datetime, random, humanfriendly, json, asyncio
import time as pyTime
from config import COLOR_EMBED, NAME, IMAGE_LINK, GEmoji
from .Json_files import userdata, giveawayData

class ButtonGiveaway(nextcord.ui.View):
	def __init__(self, user: nextcord.Member, time, msg=None):
		super().__init__(timeout=int(time))
		self.user = user
		self.message = msg

	async def on_timeout(self):
	    for child in self.children:
	       child.disabled = True
	    await self.message.edit(view=self)
	
	@nextcord.ui.button(label="Join giveaway", style=ButtonStyle.green, emoji="<a:giveaway:1144793184455630888>", custom_id="givejoin")
	async def Joins(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
		
		data = await giveawayData()
		accounts = await userdata()
		
		if str(interaction.user.id) not in accounts:
		  		embed = Embed(title="**Something is wrong**", color=COLOR_EMBED)
		  		embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
		  		embed.description = f">>> **Your account it`s not activated\nPlease run slash command: `/verifie` **"
		  		embed.set_thumbnail(url=IMAGE_LINK["!"])
		  		await interaction.response.send_message(embed=embed, ephemeral=True)
		  		return
		
		if interaction.user.id in data[str(self.user.id)]["participants"]:
			return await interaction.response.send_message("**You are actually joined in the giveaway**", ephemeral=True)
		elif interaction.user.id not in data[str(self.user.id)]["participants"]:
			data[str(self.user.id)]["participants"].append(interaction.user.id)
			json.dump(data, open("./data/giveaways.json", "w"), indent=2)
			joins = [users for users in data[str(self.user.id)]["participants"]]
			await self.message.edit(content=f">>> **@here\nJoins: ```{len(joins)}```**")
			return await interaction.response.send_message("**You have a join the giveaway successfuly**", ephemeral=True)
		else:
			return interaction.response.send_message("**Sorry this giveaway actually its ended**", ephemeral=True)



async def GiveawayStart(interaction: Interaction, winners: int, prize: str, end: str = None, channel=None, desc: str=None, mention=None):
	
	data = await giveawayData()
	
	user = interaction.user
	if mention == None:
		mention = ""
	if channel == None:
		channel = interaction.channel
	if desc == None:
		desc = "Non description....."
	if end == None:
		end = "10m"
	if str(user.id) in data:
		give_channel = interaction.guild.get_channel(int(data[str(user.id)]["channel"]))
		embed = Embed(color=COLOR_EMBED, title=f"**Sorry, {user.mention}**")
		embed.description =f"**Actually you have a giveaway in {give_channel.mention}**"
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	
	time = humanfriendly.parse_timespan(end)
	end_time = pyTime.time() + time
	
	embed = Embed(title=f"{GEmoji['for-title']} Giveaway start {GEmoji['for-title']}" ,color=COLOR_EMBED)
	embed.description =f">>> **{GEmoji['Hosted']} Hosted by: {user.mention}\n{GEmoji['time']} Ends: <t:{int(end_time)}:R>\n{GEmoji['winners']} Winners: `{winners}`\n{GEmoji['giveaway']} Prize: `{prize}`**"
	embed.add_field(name="Description", value=f">>> ```{desc}```")
	embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/912629091650400307.png")
	embed.set_author(name=NAME + " | Gifts", icon_url=IMAGE_LINK["icon"])
	
	await interaction.response.send_message(f"**The giveaway started - {channel.mention}**", ephemeral=True)
	
	msg = await channel.send(f"{mention}", embed=embed, view=ButtonGiveaway(user=interaction.user, time=end_time))
		
	data[str(interaction.user.id)] = {}
	data[str(interaction.user.id)]["channel"] = channel.id
	data[str(interaction.user.id)]["prize"] = str(prize)
	data[str(interaction.user.id)]["message"] = msg.id
	data[str(interaction.user.id)]["winners"] = str(winners)
	data[str(interaction.user.id)]["participants"] = []
	data[str(interaction.user.id)]["time"] = end_time
	data[str(interaction.user.id)]["desc"] = desc
	with open("./data/giveaways.json", "w") as f:
		json.dump(data, f, indent=2)

	
async def GiveawayChack(bot: commands.Bot):
	
	embed = Embed(color=COLOR_EMBED)
	data = await giveawayData()
	
	for give_id in list(data.keys()):
			if pyTime.time() >= data[str(give_id)]["time"]:
				try:
					channel_id = data[str(give_id)]["channel"]
					message_id = data[str(give_id)]["message"]
					channel = await bot.fetch_channel(int(channel_id))
					message = await channel.fetch_message(int(message_id))
					host = await bot.fetch_user(int(give_id))
					participants = []
					end = data[str(give_id)]["time"]
					prize = data[str(give_id)]["prize"]
					desc = data[str(give_id)]["desc"]
					joins = data[str(give_id)]["participants"]
					for users in joins:
						get_user = await bot.fetch_user(users)
						participants.append(get_user)
					
					if len(participants) == 0:
						ListWinners = []
					else:
						if len(participants) <= int(data[str(give_id)]["winners"]):
							ListWinners = random.sample(participants, len(participants))
						else:
							ListWinners = random.sample(participants, int(data[str(give_id)]["winners"]))
					
					if len(ListWinners) == 0:
						embed.title=f"{GEmoji['for-title']} Giveaway Ended {GEmoji['for-title']}"
						embed.description =f">>> **{GEmoji['Hosted']} Hosted by: {host.mention}\n{GEmoji['time']} Ended in: <t:{int(end)}:f>\n{GEmoji['winners']} Winners: `Non winners`\n{GEmoji['giveaway']} Prize: `{prize}`**"
						embed.add_field(name="Description", value=f">>> ```{desc}```")
						embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1183525262713958532.png")
						embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
						embed.set_footer(text=f"Winners: {len(participants)}")
						view = ButtonGiveaway(user=host, time=1, msg=message)
						await message.edit(embed=embed, view=view)
					else:
						winner = " • ".join(x.mention for x in ListWinners)
						embed.title=f"{GEmoji['for-title']} Giveaway Ended {GEmoji['for-title']}"
						embed.description =f">>> **{GEmoji['Hosted']} Hosted by: {host.mention}\n{GEmoji['time']} Ended in: <t:{int(end)}:f>\n{GEmoji['winners']} Winners: {winner}\n{GEmoji['giveaway']} Prize: `{prize}`**"
						embed.add_field(name="Description", value=f">>> ```{desc}```")
						embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1183525262713958532.png")
						embed.set_author(name=NAME, icon_url=IMAGE_LINK["icon"])
						embed.set_footer(text=f"Winners: {len(participants)}")
						view = ButtonGiveaway(user=host, time=1, msg=message)
						await message.edit(embed=embed, view=view)
						congrats = Embed(color=COLOR_EMBED, title=f"**{GEmoji['Congrats']} Prize: `{prize}` {GEmoji['Congrats']}**",description=f"**Winners!\n{winner}**")
						congrats.set_thumbnail(url="https://cdn.discordapp.com/emojis/928666622691004467.png")
						await channel.send(f"** Hi {host.mention} the giveaway is over <:Think:1196170601023406126>**", embed=congrats)
						
					del data[str(give_id)]
					with open("./data/giveaways.json", "w") as f:
						json.dump(data, f, indent=2)
				except Exception as E:
					for give_id in data:
						user = await bot.fetch_user(int(give_id))
						channel_id = data[str(give_id)]["channel"]
						message_id = data[str(give_id)]["message"]
						channel = await bot.fetch_channel(int(channel_id))
						message = await channel.fetch_message(int(message_id))
						embed.title = f"**something wrong**"
						embed.description = f">>> **the giveaway deleted...\n\nReason: ```{E}```**"
						embed.set_thumbnail(url=IMAGE_LINK["!"])
						view = ButtonGiveaway(user=user, time=1, msg=message)
						await message.edit(embed=embed, view=view, delete_after=120)
						await channel.send(f"** {user.mention}\nDelete after.....<f:{int(pyTime.time()+120)}:R>**", delete_after=120)
						await asyncio.sleep(10)
						await message.delete()
						del data[str(give_id)]
						with open("./data/giveaways.json", "w") as f:
							json.dump(data, f, indent=2)
			else:
				pass


#Update ButtonGiveaway
async def GiftButtonUpdate(bot: commands.Bot):
	
	data = await giveawayData()
	
	try:
		for user_id in data:
			
			channel_id = data[str(user_id)]["channel"]
			message_id = data[str(user_id)]["message"]
			time = data[str(user_id)]["time"]
			
			channel = await bot.fetch_channel(int(channel_id))
			message = await channel.fetch_message(int(message_id))
			user = await bot.fetch_user(int(user_id))
			
			await message.edit(view=ButtonGiveaway(user=user, time=int(time), msg=message))
	except Exception as E:
		print(E)
